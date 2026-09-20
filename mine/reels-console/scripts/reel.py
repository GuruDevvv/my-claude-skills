# -*- coding: utf-8 -*-
"""reel.py — монтаж вертикального ролика из одного статичного дубля.

Делает то, что в CapCut делается руками: режет паузы, нарезает съёмку с одной точки
на разные крупности с привязкой к лицу, ставит наезды и отъезды, кладёт перебивки,
рисует титры с акцентными словами, подкладывает музыку с автоприглушением.

Требуется: ffmpeg + ffprobe в PATH, python-пакеты openai-whisper, opencv-python,
insightface (последние два нужны только для титров и привязки к лицу).

    python reel.py дубль.mp4 -o ролик.mp4 --accent впервые признателен --cta подпишись
    python reel.py дубль.mp4 --dry-run          # только план монтажа, без рендера

Полный разбор приёмов — references/recipes.md рядом.
"""
import argparse, io, json, os, re, shutil, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30


# ---------- вспомогательное ----------
def run(args, quiet=True):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("\nНе выполнилось:", " ".join(str(a) for a in args[:8]), "…")
        print((r.stderr or "")[-1500:])
        sys.exit(1)
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_type,width,height:format=duration", "-of", "json", path])
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        sys.exit("В файле нет видеодорожки: %s" % path)
    # ffprobe показывает размер как он лежит в файле; при повороте кадр придёт другим,
    # поэтому реальные пропорции берём у декодера
    r2 = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
              "-show_entries", "stream_side_data=rotation", "-of", "default=nw=1", path])
    rot = re.search(r"rotation=(-?\d+)", r2.stdout)
    w, h = v["width"], v["height"]
    if rot and abs(int(rot.group(1))) % 180 == 90:
        w, h = h, w
    return dict(w=w, h=h, dur=float(d["format"]["duration"]), audio=bool(a))


# ---------- 1. паузы ----------
def detect_silences(path, min_pause):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-af",
                        "silencedetect=noise=-32dB:d=%.2f" % min_pause, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    if len(ends) < len(starts):
        ends.append(probe(path)["dur"])
    return list(zip(starts, ends))


def keep_segments(dur, silences, min_pause, keep):
    cuts = []
    for s, e in silences:
        if e - s <= min_pause:
            continue
        a, b = s + keep / 2, e - keep / 2
        if b - a > 0.05:
            cuts.append((a, b))
    segs, pos = [], 0.0
    for a, b in cuts:
        if a > pos + 0.05:
            segs.append((pos, a))
        pos = b
    if dur > pos + 0.05:
        segs.append((pos, dur))
    return segs


def cut_pauses(src, segs, out):
    fc, parts = [], []
    for i, (s, e) in enumerate(segs):
        fc.append("[0:v]trim=%s:%s,setpts=PTS-STARTPTS[v%d];" % (s, e, i))
        fc.append("[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS[a%d];" % (s, e, i))
        parts.append("[v%d][a%d]" % (i, i))
    fc.append("".join(parts) + "concat=n=%d:v=1:a=1[v][a]" % len(segs))
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", "".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-c:a", "aac", "-b:a", "192k", out])


def remap(t, segs):
    acc = 0.0
    for s, e in segs:
        if t < s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


# ---------- 2. речь ----------
def transcribe(wav, model_name, lang, cache):
    if os.path.exists(cache):
        print("   расшифровка взята из кэша:", os.path.basename(cache))
        return json.load(io.open(cache, encoding="utf-8"))
    import whisper
    print("   расшифровываю (%s)…" % model_name, flush=True)
    m = whisper.load_model(model_name)
    r = m.transcribe(wav, language=lang, word_timestamps=True)
    words = [{"w": w["word"].strip(), "s": round(w["start"], 3), "e": round(w["end"], 3)}
             for seg in r["segments"] for w in seg.get("words", [])]
    d = {"text": r["text"], "words": words}
    json.dump(d, io.open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


# ---------- 3. лицо и запас кадра ----------
def face_anchor(path, at=2.0):
    """Возвращает (x, y глаз в долях кадра, предельную крупность, как нашли)."""
    tmp = os.path.join(tempfile.gettempdir(), "_reel_frame.png")
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(at), "-i", path, "-frames:v", "1", tmp])
    try:
        import cv2
    except ImportError:
        return 0.5, 0.28, 1.35, "opencv не установлен, беру центр кадра"
    img = cv2.imread(tmp)
    os.remove(tmp)
    if img is None:
        return 0.5, 0.28, 1.35, "кадр не прочитался"
    h, w = img.shape[:2]
    bb = kps = None
    how = "центр кадра"
    try:
        from insightface.app import FaceAnalysis
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640))
        faces = app.get(cv2.resize(img, (w // 3, h // 3)))
        if faces:
            f = max(faces, key=lambda x: x.bbox[2] - x.bbox[0])
            bb, kps, how = f.bbox * 3, f.kps * 3, "insightface"
    except Exception:
        pass
    if bb is None:
        cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        ff = cas.detectMultiScale(cv2.cvtColor(cv2.resize(img, (w // 3, h // 3)), cv2.COLOR_BGR2GRAY), 1.1, 5)
        if len(ff):
            x, y, fw, fh = max(ff, key=lambda r: r[2])
            bb = [x * 3, y * 3, (x + fw) * 3, (y + fh) * 3]
            how = "каскад Хаара"
    if bb is None:
        return 0.5, 0.28, 1.35, how
    eye_y = float((kps[0][1] + kps[1][1]) / 2) if kps is not None else float(bb[1] + (bb[3] - bb[1]) * 0.42)
    cx = float((kps[0][0] + kps[1][0]) / 2) if kps is not None else float((bb[0] + bb[2]) / 2)
    ax, ay = cx / w, eye_y / h
    # до какой крупности можно приближаться, не срезая макушку
    top = max(0.01, (bb[1] - (bb[3] - bb[1]) * 0.35) / h)
    zmax = 1.0
    for z in [1.0 + i * 0.05 for i in range(1, 25)]:
        ch = 1.0 / z
        y = min(max(0.0, ay - ch / 3), 1 - ch)
        if y > top:
            break
        zmax = z
    return ax, ay, round(zmax, 2), how


# ---------- 4. план ----------
def plan_shots(words, dur, accent, zmax, max_shot=3.4, min_shot=1.4):
    bounds = [0.0]
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] >= 0.10 and b["s"] - bounds[-1] >= 1.5:
            bounds.append(round(b["s"] - 0.06, 3))
    bounds.append(dur)
    merged = [bounds[0]]
    for i, t in enumerate(bounds[1:]):
        if t - merged[-1] < min_shot and i != len(bounds) - 2:
            continue
        merged.append(t)
    split = [merged[0]]
    for a, b in zip(merged, merged[1:]):
        n = int((b - a) // max_shot)
        for k in range(1, n + 1):
            want = a + (b - a) * k / (n + 1)
            near = min(words, key=lambda w: abs(w["s"] - want))["s"] if words else want
            if near - split[-1] > 1.2 and b - near > 1.2:
                split.append(near)
        split.append(b)
    mid = 1.0 + (zmax - 1.0) * 0.45
    cycle = [1.0, round(mid, 2), round(zmax, 2), round(mid, 2)]
    shots = []
    for i, (s, e) in enumerate(zip(split, split[1:])):
        shots.append(dict(s=s, e=e, z=cycle[i % 4], move="slow" if e - s > 3.2 else "none"))
    if shots:
        shots[-1].update(z=1.0, move="pullout")
        for sh in shots:
            if any(sh["s"] <= w["s"] < sh["e"] and w["norm"] in accent for w in words):
                sh.update(move="punch", z=max(sh["z"], round(1.0 + (zmax - 1.0) * 0.8, 2)))
                break
    return shots


# ---------- 5. рендер ----------
def crop_expr(z, ax, ay):
    cw, ch = "trunc(iw/%s/2)*2" % z, "trunc(ih/%s/2)*2" % z
    return "crop=%s:%s:max(0\\,min(iw-%s\\,%s*iw-%s/2)):max(0\\,min(ih-%s\\,%s*ih-%s/3))" % (
        cw, ch, cw, ax, cw, ch, ay, ch)


def zp(z_expr, ax, ay, fps):
    return ("zoompan=z='%s':d=1:x='%s*iw-(iw/zoom/2)':y='%s*ih-(ih/zoom/3)':s=%dx%d:fps=%d"
            % (z_expr, ax, ay, W, H, fps))


def render_shots(src, shots, ax, ay, outdir, zmax=None):
    """zmax — предельная крупность кадра: выше неё срезается макушка, поэтому
    все движения зажимаются в коридор [1.0, zmax]. Если коридора нет, движения нет."""
    zmax = zmax or max(sh["z"] for sh in shots)
    room = zmax > 1.03
    files = []
    for i, sh in enumerate(shots):
        f = os.path.join(outdir, "shot%02d.mp4" % i)
        dur = sh["e"] - sh["s"]
        if sh["move"] == "punch" and dur > 0.35 and room:
            p = os.path.join(outdir, "shot%02dp.mp4" % i)
            z0, z1 = max(1.0, round(sh["z"] / 1.45, 3)), min(sh["z"], zmax)
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(sh["s"]), "-t", "0.2", "-i", src, "-vf",
                 "fps=180," + zp("%s+(%s-%s)*on/35" % (z0, z1, z0), ax, ay, 180) +
                 ",tmix=frames=6,fps=%d,setsar=1,format=yuv420p" % FPS,
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", p])
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(sh["s"] + 0.2), "-t", str(dur - 0.2), "-i", src,
                 "-vf", "%s,scale=%d:%d,setsar=1,format=yuv420p" % (crop_expr(sh["z"], ax, ay), W, H),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", f])
            files += [p, f]
            continue
        if sh["move"] in ("slow", "pullout") and room:
            n = max(2, int(dur * FPS) - 1)
            if sh["move"] == "slow":
                z0, z1 = sh["z"], min(sh["z"] * 1.08, zmax)
            else:
                z0, z1 = min(sh["z"] * 1.10, zmax), sh["z"]
            vf = zp("%s+(%s-%s)*on/%d" % (round(z0, 3), round(z1, 3), round(z0, 3), n), ax, ay, FPS) + \
                 ",setsar=1,format=yuv420p"
        else:
            vf = "%s,scale=%d:%d,setsar=1,format=yuv420p" % (crop_expr(sh["z"], ax, ay), W, H)
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(sh["s"]), "-t", str(dur), "-i", src,
             "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", f])
        files.append(f)
    return files


def concat(files, out, workdir):
    lst = os.path.join(workdir, "_concat.txt")
    io.open(lst, "w", encoding="utf-8").write(
        "".join("file '%s'\n" % os.path.abspath(p).replace("\\", "/") for p in files))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])


def put_brolls(base, brolls, out):
    if not brolls:
        run(["ffmpeg", "-y", "-v", "error", "-i", base, "-c", "copy", out])
        return
    ins, fc, prev = [], [], "[0:v]"
    for i, (path, at, length) in enumerate(brolls):
        ins += ["-i", path]
        fc.append("[%d:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
                  "trim=0:%s,setpts=PTS-STARTPTS+%s/TB[b%d];" % (i + 1, W, H, W, H, length, at, i))
        lbl = "[v]" if i == len(brolls) - 1 else "[vb%d]" % i
        fc.append("%s[b%d]overlay=enable='between(t,%s,%s)'%s;" % (prev, i, at, at + length, lbl))
        prev = lbl
    run(["ffmpeg", "-y", "-v", "error", "-i", base] + ins +
        ["-filter_complex", "".join(fc).rstrip(";"), "-map", "[v]", "-map", "0:a?",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "copy", out])


# ---------- 6. титры ----------
ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Base,{font},58,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,0,2,90,90,300,204
Style: Accent,{font_bold},118,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,0,2,60,60,540,204
Style: Cta,{font_bold},132,{cta_colour},&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,0,2,60,60,540,204

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def gen_ass(words, accent, cta, path, font, font_bold, cta_colour):
    def ts(x):
        return "%d:%02d:%05.2f" % (int(x // 3600), int(x % 3600 // 60), x % 60)

    lines, buf, ev = [], [], []
    for w in words:
        buf.append(w)
        if len(buf) == 3 or w["w"].endswith((",", ".", "?", "!")):
            lines.append(buf)
            buf = []
    if buf:
        lines.append(buf)
    pop = "{\\fscx55\\fscy55\\t(0,130,\\fscx100\\fscy100)}"
    for ln in lines:
        big = [x for x in ln if x["norm"] in accent or x["norm"] in cta]
        base = " ".join(x["w"] for x in ln if x not in big)
        if base.strip():
            ev.append("Dialogue: 0,%s,%s,Base,,0,0,0,,%s" % (ts(ln[0]["s"]), ts(ln[-1]["e"] + 0.15), base))
        for x in big:
            st = "Cta" if x["norm"] in cta else "Accent"
            ev.append("Dialogue: 1,%s,%s,%s,,0,0,0,,%s%s"
                      % (ts(x["s"]), ts(x["e"] + 0.5), st, pop, x["norm"].upper()))
    io.open(path, "w", encoding="utf-8").write(
        ASS_HEAD.format(w=W, h=H, font=font, font_bold=font_bold, cta_colour=cta_colour)
        + "\n".join(ev) + "\n")
    return [x for ln in lines for x in ln if x["norm"] in accent or x["norm"] in cta]


# ---------- 7. звук ----------
def mix_audio(video, voice_src, music, sfx, out):
    ins = ["-i", video, "-i", voice_src]
    # asplit нужен только чтобы отдать голос в боковую цепь компрессора под музыку;
    # без музыки второй выход останется висеть, и ffmpeg откажется собирать граф
    fc = ["[1:a]aformat=fltp:44100:stereo,asplit=2[sc][voice];" if music
          else "[1:a]aformat=fltp:44100:stereo[voice];"]
    mixed = ["[voice]"]
    idx = 2
    if music:
        ins += ["-i", music]
        fc.append("[%d:a]aformat=fltp:44100:stereo,volume=%s[m];" % (idx, "0.25"))
        fc.append("[m][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[mduck];")
        mixed.append("[mduck]")
        idx += 1
    for path, t, vol in sfx:
        ins += ["-i", path]
        ms = int(t * 1000)
        fc.append("[%d:a]aformat=fltp:44100:stereo,adelay=%d|%d,volume=%s[s%d];" % (idx, ms, ms, vol, idx))
        mixed.append("[s%d]" % idx)
        idx += 1
    if len(mixed) == 1:
        fc.append("[voice]anull[a]")
    else:
        fc.append("".join(mixed) + "amix=inputs=%d:duration=first:normalize=0,alimiter=limit=0.95[a]" % len(mixed))
    run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", "".join(fc),
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])


def contact_sheet(video, out, cols=6, rows=2):
    dur = probe(video)["dur"]
    step = max(0.5, dur / (cols * rows))
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf",
         "fps=1/%.3f,scale=200:356,tile=%dx%d" % (step, cols, rows), "-frames:v", "1", out])


# ---------- сборка ----------
def parse_broll(s):
    # формат: файл@секунда:длительность
    m = re.match(r"^(.*)@([\d.]+):([\d.]+)$", s)
    if not m:
        sys.exit("Перебивка пишется так: файл.mp4@7.5:1.8 (файл, секунда, длительность)")
    return m.group(1), float(m.group(2)), float(m.group(3))


def norm_word(s):
    return re.sub(r"[^\w\-]", "", s, flags=re.U).lower()


def main():
    ap = argparse.ArgumentParser(description="Монтаж вертикального ролика из одного статичного дубля")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--accent", nargs="*", default=[], help="2–4 слова, которые покажем крупно")
    ap.add_argument("--cta", nargs="*", default=[], help="слово-призыв, покажем цветом")
    ap.add_argument("--broll", nargs="*", default=[], help="перебивка: файл.mp4@7.5:1.8")
    ap.add_argument("--music", default=None)
    ap.add_argument("--whoosh", default=None, help="звук на наезд и отъезд")
    ap.add_argument("--pop", default=None, help="звук на появление акцентного слова")
    ap.add_argument("--lang", default="ru")
    ap.add_argument("--model", default="small", help="модель whisper: tiny/base/small/medium")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--font-bold", default="Arial Black")
    ap.add_argument("--cta-colour", default="&H0033E5C6", help="цвет CTA в формате ASS (&H00BBGGRR)")
    ap.add_argument("--min-pause", type=float, default=0.45, help="паузы длиннее режем")
    ap.add_argument("--keep-pause", type=float, default=0.18, help="сколько паузы оставляем")
    ap.add_argument("--no-subs", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="только показать план монтажа")
    ap.add_argument("--workdir", default=None)
    a = ap.parse_args()

    src = os.path.abspath(a.input)
    if not os.path.exists(src):
        sys.exit("Нет файла: " + src)
    out = os.path.abspath(a.output or os.path.splitext(src)[0] + "-reel.mp4")
    work = os.path.abspath(a.workdir or os.path.splitext(src)[0] + "-work")
    os.makedirs(os.path.join(work, "shots"), exist_ok=True)
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit("Нет %s в PATH" % tool)

    info = probe(src)
    print("исходник: %dx%d, %.1f с, звук %s" % (info["w"], info["h"], info["dur"], "есть" if info["audio"] else "НЕТ"))
    if info["w"] > info["h"]:
        print("  ! кадр горизонтальный: вертикаль вырежется из середины, запас на приближение будет мал")

    print("1. паузы")
    sil = detect_silences(src, a.min_pause)
    segs = keep_segments(info["dur"], sil, a.min_pause, a.keep_pause)
    tight = os.path.join(work, "tight.mp4")
    if not a.dry_run:
        cut_pauses(src, segs, tight)
        tdur = probe(tight)["dur"]
    else:
        tdur = sum(e - s for s, e in segs)
    print("   %.1f с -> %.1f с, пауз найдено %d" % (info["dur"], tdur, len(sil)))

    print("2. речь")
    words = []
    if info["audio"] and not a.no_subs:
        wav = os.path.join(work, "speech.wav")
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav])
        d = transcribe(wav, a.model, a.lang, os.path.join(work, "words.json"))
        for w in d["words"]:
            nw = dict(w, s=remap(w["s"], segs), e=remap(w["e"], segs), norm=norm_word(w["w"]))
            if nw["e"] > nw["s"]:
                words.append(nw)
        print("   слов: %d" % len(words))
    else:
        print("   пропущено")

    print("3. лицо и запас кадра")
    ax, ay, zmax, how = face_anchor(src)
    print("   глаза x=%.2f y=%.2f (%s), предельная крупность %.2f" % (ax, ay, how, zmax))
    if zmax < 1.25:
        print("   ! СНЯТО СЛИШКОМ БЛИЗКО: приближаться некуда, смены крупности почти не будет.")
        print("     Для следующего дубля встаньте в 1,5–2 м от камеры.")

    accent = {norm_word(x) for x in a.accent}
    cta = {norm_word(x) for x in a.cta}
    print("4. план")
    shots = plan_shots(words, tdur, accent, zmax)
    moves = {"none": "статичный", "slow": "медленный наезд", "punch": "ударный наезд",
             "pullout": "отъезд"}
    for i, sh in enumerate(shots):
        mv = moves[sh["move"]] if zmax > 1.03 else "статичный (нет запаса кадра)"
        print("   %2d: %5.1f–%5.1f  крупность %.2f  %s" % (i, sh["s"], sh["e"], sh["z"], mv))
    if a.dry_run:
        return

    print("5. рендер планов")
    files = render_shots(tight, shots, ax, ay, os.path.join(work, "shots"), zmax)
    v_shots = os.path.join(work, "v_shots.mp4")
    concat(files, v_shots, work)

    print("6. перебивки")
    v_broll = os.path.join(work, "v_broll.mp4")
    put_brolls(v_shots, [parse_broll(b) for b in a.broll], v_broll)

    print("7. титры")
    v_subs = v_broll
    hits = []
    if words:
        ass = os.path.join(work, "subs.ass")
        hits = gen_ass(words, accent, cta, ass, a.font, a.font_bold, a.cta_colour)
        v_subs = os.path.join(work, "v_subs.mp4")
        cwd = os.getcwd()
        os.chdir(work)  # у фильтра subtitles путь с двоеточием диска ломается
        run(["ffmpeg", "-y", "-v", "error", "-i", v_broll, "-vf", "subtitles=subs.ass,format=yuv420p",
             "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-c:a", "copy", v_subs])
        os.chdir(cwd)

    print("8. звук")
    sfx = []
    if a.whoosh:
        sfx += [(a.whoosh, sh["s"], "0.45") for sh in shots if sh["move"] in ("punch", "pullout")]
    if a.pop:
        sfx += [(a.pop, w["s"], "0.30") for w in hits]
    mix_audio(v_subs, tight, a.music, sfx, out)

    sheet = os.path.splitext(out)[0] + "-sheet.png"
    contact_sheet(out, sheet)
    print("\nготово: %s  (%.1f с)" % (out, probe(out)["dur"]))
    print("раскадровка: %s — посмотрите её прежде чем открывать ролик" % sheet)


if __name__ == "__main__":
    main()
