# -*- coding: utf-8 -*-
"""reel.py — монтаж вертикального ролика из одного статичного дубля.

Делает то, что в CapCut делается руками: режет паузы, нарезает съёмку с одной точки
на разные крупности с привязкой к лицу, ставит наезды и отъезды, кладёт перебивки,
рисует титры с акцентными словами, подкладывает музыку с автоприглушением.

Требуется: ffmpeg + ffprobe в PATH, python-пакеты openai-whisper, opencv-python,
insightface (последние два нужны только для титров и привязки к лицу).

    python reel.py дубль.mp4 -o ролик.mp4 --accent впервые признателен --cta подпишись
    python reel.py дубль.mp4 --dry-run          # только план монтажа, без рендера
    python reel.py дубль.mp4 --frame --lut look.cube --flash   # «ролик в рамке», цвет, засвет

Полный разбор приёмов — references/recipes.md рядом.
"""
import argparse, io, json, os, re, shutil, subprocess, sys, tempfile

CW, CH = 1080, 1920          # холст готового ролика
W, H, FPS = CW, CH, 30       # размер, в котором рендерятся планы; в режиме рамки — окно
# окно «ролика в рамке»: 4:5 почти во всю ширину, по центру, скругление 50 px
FRAME = dict(w=1030, h=1288, r=50)


# ---------- вспомогательное ----------
def run(args, quiet=True, cwd=None):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
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


def keep_segments(dur, silences, min_pause, keep, drops=()):
    cuts = list(drops)  # куски, которые человек велел выбросить целиком (вздох, оговорка)
    for s, e in silences:
        if e - s <= min_pause:
            continue
        a, b = s + keep / 2, e - keep / 2
        if b - a > 0.05:
            cuts.append((a, b))
    segs, pos = [], 0.0
    for a, b in sorted(cuts):
        if a > pos + 0.05:
            segs.append((pos, a))
        pos = max(pos, b)
    if dur > pos + 0.05:
        segs.append((pos, dur))
    return segs


def cut_pauses(src, segs, out, speed=1.0):
    fc, parts = [], []
    for i, (s, e) in enumerate(segs):
        fc.append("[0:v]trim=%s:%s,setpts=PTS-STARTPTS[v%d];" % (s, e, i))
        # короткие затухания на каждой склейке: без них стык щёлкает
        fc.append("[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=%.3f:d=0.015[a%d];"
                  % (s, e, max(0.0, e - s - 0.015), i))
        parts.append("[v%d][a%d]" % (i, i))
    if speed == 1.0:
        fc.append("".join(parts) + "concat=n=%d:v=1:a=1[v][a]" % len(segs))
    else:
        # atempo меняет темп без изменения высоты голоса
        fc.append("".join(parts) + "concat=n=%d:v=1:a=1[vc][ac];[vc]setpts=PTS/%s,fps=%d[v];[ac]atempo=%s[a]"
                  % (len(segs), speed, FPS, speed))
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", "".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-c:a", "aac", "-b:a", "192k", out])


def remap(t, segs, speed=1.0):
    acc = 0.0
    for s, e in segs:
        if t < s:
            break
        if t <= e:
            acc += t - s
            break
        acc += e - s
    return acc / speed


def envelope(wav, win=0.01):
    """Громкость звука по окнам 10 мс, дБ от полной шкалы. Вход — моно 16 бит."""
    import array, math, wave
    with wave.open(wav, "rb") as f:
        rate, data = f.getframerate(), array.array("h", f.readframes(f.getnframes()))
    n = int(rate * win)
    return [10 * math.log10(sum(x * x for x in data[i:i + n]) / (n * 32768.0 ** 2) + 1e-10)
            for i in range(0, len(data) - n, n)]


def check_cuts(env, segs, drops=(), win=0.01):
    """Склейки по звуку: край внутри слова, тихий слог в вырезанной паузе."""
    if not env:
        return []
    lv = sorted(env)
    thr = min(-30.0, lv[int(len(lv) * 0.95)] - 20)
    floor = lv[int(len(lv) * 0.10)]
    notes = []

    def loud_near(t, side):
        i0 = int(t / win)
        rng = range(i0, min(len(env), i0 + 30)) if side > 0 else range(max(0, i0 - 30), i0)
        hot = [abs(i - i0) * win for i in rng if env[i] >= thr]
        return len(hot) >= 15 and min(hot) <= 0.08

    for k, (s, e) in enumerate(segs):
        if k and loud_near(s, -1):
            notes.append("склейка на %.2f с: звук идёт прямо до края, возможно срезано начало слова" % s)
        if k < len(segs) - 1 and loud_near(e, +1):
            notes.append("склейка на %.2f с: звук продолжается за краем, возможно срезан конец слова" % e)
    for (_, a), (b, _) in zip(segs, segs[1:]):
        if any(ds < b and a < de for ds, de in drops):
            continue  # этот кусок выброшен человеком, он знает, что там
        run_len = best = 0
        for i in range(int(a / win), min(len(env), int(b / win))):
            run_len = run_len + 1 if max(thr - 8, floor + 10) <= env[i] < thr else 0
            best = max(best, run_len)
        if best * win >= 0.08:
            notes.append("в вырезанной паузе %.2f–%.2f с есть тихий звук, возможно слог: послушайте" % (a, b))
    return notes


def wordless_speech(silences, raw_words, dur):
    """Куски, где звук есть, а слов в расшифровке нет: вздох, оговорка, потерянная фраза."""
    out, pos = [], 0.0
    for s, e in list(silences) + [(dur, dur)]:
        if s - pos >= 0.4 and not any(pos - 0.15 <= (w["s"] + w["e"]) / 2 <= s + 0.15 for w in raw_words):
            out.append((round(pos, 2), round(s, 2)))
        pos = e
    return out


# ---------- 2. речь ----------
_WHISPER = {}


def whisper_words(wav, model_name, lang, offset=0.0, fresh=False):
    import whisper
    if model_name not in _WHISPER:
        _WHISPER[model_name] = whisper.load_model(model_name)
    kw = dict(condition_on_previous_text=False) if fresh else {}
    r = _WHISPER[model_name].transcribe(wav, language=lang, word_timestamps=True, **kw)
    words = []
    for w in (w for seg in r["segments"] for w in seg.get("words", [])):
        t = w["word"].strip()
        if t.startswith("-") and words:  # «какие» + «-то» приходят двумя кусками
            words[-1].update(w=words[-1]["w"] + t, e=round(w["end"] + offset, 3))
        elif t:
            words.append({"w": t, "s": round(w["start"] + offset, 3), "e": round(w["end"] + offset, 3)})
    return r["text"], words


# фразы, которые whisper выдумывает на тишине и обрывках
HALLUCINATIONS = ("субтитр", "продолжение следует", "редактор", "корректор", "спасибо за просмотр")


def recheck(words, wav, model_name, lang, pauses, dur, work):
    """Слово длиннее секунды — признак, что распознавание склеило или потеряло кусок речи.
    Такие места переслушиваются отдельным куском до 5 с, без контекста всего ролика."""
    sus = [w for w in words if w["e"] - w["s"] > 1.0 or w["e"] <= w["s"]]
    if not sus:
        return words, []
    mids = [(s + e) / 2 for s, e in pauses]
    regions = []
    for w in sus:
        a = max([m for m in mids if m <= w["s"]] or [max(0.0, w["s"] - 0.5)])
        b = min([m for m in mids if m >= w["e"]] or [min(dur, w["e"] + 0.5)])
        if regions and a <= regions[-1][1]:
            regions[-1][1] = max(regions[-1][1], b)
        else:
            regions.append([a, b])
    changes = []
    key = lambda w: norm_word(w["w"])[:5]
    longest = lambda ws: max([w["e"] - w["s"] for w in ws] or [0])
    for a, b in regions:
        pos = a
        while b - pos > 0.3:
            # кусок кончается только на паузе: обрыв посреди слова whisper дописывает выдумкой
            stops = [m for m in mids if pos + 1.0 < m <= pos + 5.0 and m <= b] or \
                    [m for m in mids if pos + 5.0 < m <= pos + 8.0 and m <= b][:1]
            end = stops[-1] if stops else min(b, pos + 5.0)
            clip = os.path.join(work, "_recheck.wav")
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(pos), "-t", str(end - pos), "-i", wav, clip])
            text, new = whisper_words(clip, model_name, lang, offset=pos, fresh=True)
            old = [w for w in words if pos <= (w["s"] + w["e"]) / 2 < end]
            fake = any(h in text.lower() for h in HALLUCINATIONS)
            if new and not fake and (len(new) > len(old) or (len(new) == len(old) and longest(new) < longest(old))):
                # слово, которое распознавание раньше поставило не на своё место, после переслушивания
                # появляется в куске заново, а старая копия остаётся рядом: её убираем
                fresh = {key(w) for w in new} - {key(w) for w in old}
                stray = [w for w in words if w not in old and key(w) in fresh
                         and pos - 4.0 <= (w["s"] + w["e"]) / 2 <= end + 4.0]
                # написание и знаки берутся из полной расшифровки: на обрывке окончания хуже
                spell = {key(w): w["w"] for w in stray + old}
                for w in new:
                    w["w"] = spell.get(key(w), w["w"].rstrip(".").rstrip("…"))
                if [w["w"] for w in new] != [w["w"] for w in old]:
                    changes.append("%.1f–%.1f с: было «%s», стало «%s»"
                                   % (pos, end, " ".join(w["w"] for w in old), " ".join(w["w"] for w in new)))
                words = sorted([w for w in words if w not in old and w not in stray] + new, key=lambda w: w["s"])
            pos = end
    return words, changes


def snap_words(raw, segs, drops):
    """Распознавание часто ставит короткое слово в паузу рядом с ним. После вырезания паузы
    такое слово пропало бы из титров, поэтому оно сдвигается в ближайший оставленный кусок.
    Слова из выброшенных вручную кусков убираются."""
    out = []
    for w in raw:
        mid, d = (w["s"] + w["e"]) / 2, w["e"] - w["s"]
        if any(a <= mid <= b for a, b in drops):
            continue
        for (_, a), (b, _) in zip(segs, segs[1:]):
            if a < mid < b:
                w = dict(w, s=a - d, e=a) if mid - a < b - mid else dict(w, s=b, e=b + d)
                break
        out.append(w)
    return sorted(out, key=lambda w: w["s"])


def transcribe(wav, model_name, lang, cache, pauses=(), dur=0.0, check=True):
    if os.path.exists(cache):
        d = json.load(io.open(cache, encoding="utf-8"))
        if d.get("rechecked") or not check:
            print("   расшифровка взята из кэша:", os.path.basename(cache))
            return d
    else:
        print("   расшифровываю (%s)…" % model_name, flush=True)
        text, words = whisper_words(wav, model_name, lang)
        d = {"text": text, "words": words}
    if check:
        d["words"], d["changes"] = recheck(d["words"], wav, model_name, lang, pauses, dur, os.path.dirname(cache))
        d["rechecked"] = True
    json.dump(d, io.open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


# ---------- 3. лицо и запас кадра ----------
_DET = []


def find_face(img):
    """Рамка самого крупного лица на кадре (x0, y0, x1, y1) или None. Только детектор, без распознавания."""
    import cv2
    if not _DET:
        try:
            from insightface.app import FaceAnalysis
            app = FaceAnalysis(name="buffalo_l", allowed_modules=["detection"], providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=-1, det_size=(640, 640))
            _DET.append(app)
        except Exception:
            _DET.append(None)
    h, w = img.shape[:2]
    k = max(1, w // 540)
    small = cv2.resize(img, (w // k, h // k))
    if _DET[0] is not None:
        faces = _DET[0].get(small)
        if faces:
            return [float(v) * k for v in max(faces, key=lambda f: f.bbox[2] - f.bbox[0]).bbox]
        return None
    cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    ff = cas.detectMultiScale(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY), 1.1, 5)
    if len(ff):
        x, y, fw, fh = max(ff, key=lambda r: r[2])
        return [x * k, y * k, (x + fw) * k, (y + fh) * k]
    return None


def scan_faces(video, step=0.5):
    """Где лицо в готовой картинке: [(секунда, x0, y0, x1, y1)]. Нужен для места титров и проверки."""
    try:
        import cv2
    except ImportError:
        return []
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out = []
    for n in range(0, total, max(1, int(fps * step))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ok, img = cap.read()
        if not ok:
            break
        bb = find_face(img)
        if bb:
            out.append((round(n / fps, 2),) + tuple(bb))
    cap.release()
    return out


def face_overlaps(faces, bands, gap=10):
    """Секунды, где подбородок заходит на полосу титров. bands: [(с, по, верх, низ)]."""
    bad = sorted({t for t, x0, y0, x1, y1 in faces for s, e, top, bot in bands
                  if s <= t <= e and y1 > top + gap and y0 < bot})
    ranges = []
    for t in bad:
        if ranges and t - ranges[-1][1] <= 0.6:
            ranges[-1][1] = t
        else:
            ranges.append([t, t])
    return ranges


def pick_cover(video, seams, out, at=None, sheet=None):
    """Обложка: кадр на стыке вырезанной паузы, там человек молчит и рот чаще закрыт.
    Из первых стыков берётся самый резкий; глаза и рот скрипт не видит — смотреть лист кандидатов."""
    cand = [at] if at is not None else (seams[:5] or [0.6, 1.2, 1.8, 2.4])
    best = cand[0]
    try:
        import cv2
        cap, shots = cv2.VideoCapture(video), []
        for t in cand:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, img = cap.read()
            if ok:
                shots.append((cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var(), t, img))
        cap.release()
        if shots:
            # самый ранний из не смазанных: резкость рот и глаза не видит, а ранний стык обычно спокойнее
            top = max(s[0] for s in shots)
            best = min(t for sharp, t, _ in shots if sharp >= 0.5 * top and (t >= 0.3 or len(shots) == 1))
            if sheet and len(shots) > 1:
                cv2.imwrite(sheet, cv2.hconcat([cv2.resize(s[2], (270, 480)) for s in sorted(shots, key=lambda s: s[1])]))
    except ImportError:
        pass
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(best), "-i", video, "-frames:v", "1", "-q:v", "2", out])
    return best, sorted(cand)


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
    # высота окна считается от ширины: так кроп не искажает пропорции,
    # даже если исходник и выход разной формы
    cw, ch = "trunc(iw/%s/2)*2" % z, "trunc(iw*%s/%s/%s/2)*2" % (H, W, z)
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


def put_brolls(base, brolls, out, speed=1.0):
    if not brolls:
        run(["ffmpeg", "-y", "-v", "error", "-i", base, "-c", "copy", out])
        return
    ins, fc, prev = [], [], "[0:v]"
    for i, (path, at, length) in enumerate(brolls):
        ins += ["-i", path]
        fc.append("[%d:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
                  "trim=0:%s,setpts=(PTS-STARTPTS)/%s+%s/TB[b%d];"
                  % (i + 1, W, H, W, H, round(length * speed, 3), speed, at, i))
        lbl = "[v]" if i == len(brolls) - 1 else "[vb%d]" % i
        fc.append("%s[b%d]overlay=enable='between(t,%s,%s)'%s;" % (prev, i, at, at + length, lbl))
        prev = lbl
    run(["ffmpeg", "-y", "-v", "error", "-i", base] + ins +
        ["-filter_complex", "".join(fc).rstrip(";"), "-map", "[v]", "-map", "0:a?",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "copy", out])


# ---------- 6. вид: цвет, засветы, рамка ----------
def make_mask(path):
    """Чёрная картинка с прозрачным скруглённым окном — кладётся поверх ролика."""
    x0, y0 = (CW - FRAME["w"]) // 2, (CH - FRAME["h"]) // 2
    x1, y1, r = x0 + FRAME["w"] - 1, y0 + FRAME["h"] - 1, FRAME["r"]
    inside = ("between(X,%d,%d)*between(Y,%d,%d)*lte(pow(max(0,max(%d-X,X-%d)),2)"
              "+pow(max(0,max(%d-Y,Y-%d)),2),%d)" % (x0, x1, y0, y1, x0 + r, x1 - r, y0 + r, y1 - r, r * r))
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=%dx%d:d=1" % (CW, CH),
         "-vf", "format=rgba,geq=r=0:g=0:b=0:a='255*(1-%s)'" % inside, "-frames:v", "1", path])


def make_flash(path):
    """Тёплый засвет из правого верхнего угла, прозрачный к краям."""
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=%dx%d:d=1" % (CW, CH),
         "-vf", "format=rgba,geq=r=255:g=205:b=150:a='255*pow(max(0,1-hypot(X-W*0.85,Y-H*0.2)/(W*1.3)),1.6)'",
         "-frames:v", "1", path])


def apply_look(base, out, work, lut=None, lut_mix=0.5, flashes=(), frame=False):
    """Цвет, засветы и рамка — одним проходом поверх готовой картинки."""
    if not (lut or flashes or frame):
        run(["ffmpeg", "-y", "-v", "error", "-i", base, "-c", "copy", out])
        return
    ins, fc, cur = ["-i", base], [], "[0:v]"
    if lut:
        # lut3d не переносит двоеточие диска в пути, поэтому файл кладётся в рабочую папку
        shutil.copy(lut, os.path.join(work, "look.cube"))
        fc.append("%ssplit[la][lb];[lb]lut3d=file=look.cube[lc];[la][lc]blend=all_expr='A+(B-A)*%s'[lk];"
                  % (cur, lut_mix))
        cur = "[lk]"
    if frame:
        fc.append("%sscale=%d:%d,pad=%d:%d:%d:%d:black[fr];"
                  % (cur, FRAME["w"], FRAME["h"], CW, CH, (CW - FRAME["w"]) // 2, (CH - FRAME["h"]) // 2))
        cur = "[fr]"
    if flashes:
        fpng = os.path.join(work, "flash.png")
        make_flash(fpng)
        for i, t in enumerate(flashes):
            t0 = round(max(0.0, t - 0.1), 3)
            ins += ["-loop", "1", "-framerate", str(FPS), "-t", "0.33", "-i", fpng]
            fc.append("[%d:v]format=rgba,fade=in:st=0:d=0.1:alpha=1,fade=out:st=0.12:d=0.21:alpha=1,"
                      "setpts=PTS-STARTPTS+%s/TB[f%d];%s[f%d]overlay=enable='between(t,%s,%s)':eof_action=pass[fo%d];"
                      % (i + 1, t0, i, cur, i, t0, t0 + 0.33, i))
            cur = "[fo%d]" % i
    if frame:
        mpng = os.path.join(work, "mask.png")
        make_mask(mpng)
        ins += ["-i", mpng]
        fc.append("%s[%d:v]overlay=0:0[mk];" % (cur, len(flashes) + 1))
        cur = "[mk]"
    fc.append("%sformat=yuv420p[v]" % cur)
    run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", "".join(fc), "-map", "[v]", "-map", "0:a?",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "copy", out], cwd=work)


def precrop_to_window(src, ay, out):
    """Для рамки: заранее вырезает из дубля кусок пропорций окна, глаза на 35% его высоты."""
    ch = "trunc(iw*%d/%d/2)*2" % (FRAME["h"], FRAME["w"])
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
         "crop=iw:%s:0:max(0\\,min(ih-%s\\,%s*ih-%s*0.35))" % (ch, ch, ay, ch),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "copy", out])


# ---------- 7. титры ----------
ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Base,{font},58,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,0,2,90,90,{mv_base},204
Style: Accent,{font_bold},118,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,0,2,60,60,{mv_acc},204
Style: Cta,{font_bold},132,{cta_colour},&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,0,2,60,60,{mv_acc},204
Style: Plate,{font},60,&H00141010,{cta_colour},{cta_colour},-1,0,0,0,100,100,0,0,3,14,0,7,{ml_plate},60,{mv_plate},204

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
PLATE_H = 96  # высота плашки с полями при кегле 60


def ass_ts(x):
    return "%d:%02d:%05.2f" % (int(x // 3600), int(x % 3600 // 60), x % 60)


def gen_plate(words, path, font, font_bold, colour, top, frame=False):
    """Титры плашкой: фраза до 26 знаков на цветной подложке, слова добавляются по мере речи.
    Плашка прижата к левому краю, поэтому не дёргается, когда растёт."""
    lines, buf = [], []
    for i, w in enumerate(words):
        buf.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt is None or w["w"].endswith((",", ".", "?", "!")) or nxt["s"] - w["e"] >= 0.5
                or len(" ".join(x["w"] for x in buf)) + 1 + len(nxt["w"]) > 26):
            lines.append(buf)
            buf = []
    ev, bands = [], []
    for k, ln in enumerate(lines):
        stop = min(ln[-1]["e"] + 0.35, lines[k + 1][0]["s"]) if k + 1 < len(lines) else ln[-1]["e"] + 0.35
        for i, w in enumerate(ln):
            s, e = w["s"], ln[i + 1]["s"] if i + 1 < len(ln) else stop
            if e - s > 0.01:
                ev.append("Dialogue: 0,%s,%s,Plate,,0,0,0,,%s" % (ass_ts(s), ass_ts(e), " ".join(x["w"] for x in ln[:i + 1])))
        bands.append((ln[0]["s"], stop, top - 14, top - 14 + PLATE_H))
    io.open(path, "w", encoding="utf-8").write(
        ASS_HEAD.format(w=CW, h=CH, font=font, font_bold=font_bold, cta_colour=colour, mv_base=300, mv_acc=540,
                        ml_plate=(CW - FRAME["w"]) // 2 + 60 if frame else 70, mv_plate=top)
        + "\n".join(ev) + "\n")
    return bands


def gen_ass(words, accent, cta, path, font, font_bold, cta_colour, frame=False):
    ts = ass_ts
    lines, buf, ev, bands = [], [], [], []
    mv_base, mv_acc = (400, 620) if frame else (300, 540)
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
            bands.append((ln[0]["s"], ln[-1]["e"] + 0.15, CH - mv_base - 66, CH - mv_base))
        for x in big:
            st = "Cta" if x["norm"] in cta else "Accent"
            ev.append("Dialogue: 1,%s,%s,%s,,0,0,0,,%s%s"
                      % (ts(x["s"]), ts(x["e"] + 0.5), st, pop, x["norm"].upper()))
            bands.append((x["s"], x["e"] + 0.5, CH - mv_acc - 135, CH - mv_acc))
    io.open(path, "w", encoding="utf-8").write(
        # в рамке титры поднимаются внутрь окна, иначе лягут на чёрное поле
        ASS_HEAD.format(w=CW, h=CH, font=font, font_bold=font_bold, cta_colour=cta_colour,
                        mv_base=mv_base, mv_acc=mv_acc, ml_plate=70, mv_plate=1300)
        + "\n".join(ev) + "\n")
    return [x for ln in lines for x in ln if x["norm"] in accent or x["norm"] in cta], bands


# ---------- 8. звук ----------
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


def loudness(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i, p = re.search(r"I:\s+(-?[\d.]+) LUFS", tail), re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return (float(i.group(1)) if i else None), (float(p.group(1)) if p else None)


def master(src, out, target=-14.0, cover=None):
    """Громкость к стандарту соцсетей в два прохода: первый меряет, второй ставит ровно.
    Один проход промахивается мимо цели. Видео не перекодируется, обложка вшивается миниатюрой."""
    base = "highpass=f=80,loudnorm=I=%s:TP=-1.5:LRA=11" % target
    r = subprocess.run(["ffmpeg", "-nostats", "-i", src, "-af", base + ":print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = base + ":measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true,aresample=48000" % (
        m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"])
    ins, maps = ["-i", src], ["-map", "0:v:0", "-map", "0:a:0"]
    if cover:
        ins += ["-i", cover]
        maps += ["-map", "1:v:0", "-disposition:v:1", "attached_pic"]
    run(["ffmpeg", "-y", "-v", "error"] + ins + maps + ["-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                                                        "-movflags", "+faststart", out])
    lufs, peak = loudness(out)
    ok = lufs is not None and abs(lufs - target) <= 1.0 and (peak is None or peak <= -1.0)
    return float(m["input_i"]), lufs, peak, ok


def thin_sfx(sfx, gap=2.0):
    """Не чаще одного звука в gap секунд: иначе ролик звенит, а не акцентирует."""
    kept = []
    for x in sorted(sfx, key=lambda x: x[1]):
        if not kept or x[1] - kept[-1][1] >= gap:
            kept.append(x)
    return kept


def parse_sfx(s):
    # формат: файл@секунда или файл@секунда:громкость
    m = re.match(r"^(.*)@([\d.]+)(?::([\d.]+))?$", s)
    if not m:
        sys.exit("Звук пишется так: волны.wav@7.2 или волны.wav@7.2:0.4 (файл, секунда, громкость)")
    return m.group(1), float(m.group(2)), m.group(3) or "0.5"


def pick_flashes(shots, n=2):
    """Засвет — на стык перед финальным отъездом и на стык в середине ролика."""
    cuts = [sh["s"] for sh in shots[1:] if sh["move"] != "punch"]
    if not cuts:
        return []
    picks = [cuts[-1]]
    if n > 1 and len(cuts) > 2:
        picks.insert(0, cuts[len(cuts) // 2 - 1])
    return picks[:n]


def contact_sheet(video, out, cols=6, rows=2):
    dur = probe(video)["dur"]
    step = max(0.5, dur / (cols * rows))
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-map", "0:v:0", "-vf",
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
    ap.add_argument("--frame", action="store_true", help="ролик в скруглённом окне на чёрном фоне")
    ap.add_argument("--lut", default=None, help="цвет из .cube-файла")
    ap.add_argument("--lut-mix", type=float, default=0.5, help="сила LUT 0–1; сильнее 0.6 кожа уходит в оранжевый")
    ap.add_argument("--flash", nargs="*", type=float, default=None,
                    help="засвет на стыке: без чисел — два авто, или секунды готового ролика")
    ap.add_argument("--sfx", nargs="*", default=[], help="звук вручную: файл@секунда[:громкость], напр. фон под перебивку")
    ap.add_argument("--broll-speed", type=float, default=1.0, help="0.85 — перебивки чуть медленнее, смотрятся дороже")
    ap.add_argument("--subs", choices=["classic", "plate"], default="classic",
                    help="plate — фраза на цветной плашке, слова добавляются по мере речи")
    ap.add_argument("--speed", type=float, default=1.0, help="темп речи без изменения голоса; 1.1 — чуть бодрее, выше 1.3 звучит суетливо")
    ap.add_argument("--drop", nargs="*", default=[], help="выбросить кусок исходника целиком: 37.8-39.1 (вздох, оговорка)")
    ap.add_argument("--no-recheck", action="store_true", help="не переслушивать подозрительные места расшифровки")
    ap.add_argument("--lufs", type=float, default=-14.0, help="целевая громкость готового ролика")
    ap.add_argument("--no-master", action="store_true", help="не приводить громкость к стандарту")
    ap.add_argument("--cover-at", type=float, default=None, help="секунда готового ролика для обложки")
    ap.add_argument("--no-cover", action="store_true", help="не вшивать обложку первым кадром")
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
    drops = []
    for x in a.drop:
        m = re.match(r"^([\d.]+)-([\d.]+)$", x)
        if not m:
            sys.exit("Кусок на выброс пишется так: 37.8-39.1 (секунды исходника)")
        drops.append((float(m.group(1)), float(m.group(2))))
    segs = keep_segments(info["dur"], sil, a.min_pause, a.keep_pause, drops)
    tight = os.path.join(work, "tight.mp4")
    if not a.dry_run:
        cut_pauses(src, segs, tight, a.speed)
        tdur = probe(tight)["dur"]
    else:
        tdur = sum(e - s for s, e in segs) / a.speed
    print("   %.1f с -> %.1f с, пауз найдено %d%s%s" % (
        info["dur"], tdur, len(sil), ", выброшено кусков %d" % len(drops) if drops else "",
        ", темп ×%s" % a.speed if a.speed != 1.0 else ""))

    print("2. речь")
    words, raw, warn = [], [], []
    wav = os.path.join(work, "speech.wav")
    if info["audio"]:
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])
    if info["audio"] and not a.no_subs:
        d = transcribe(wav, a.model, a.lang, os.path.join(work, "words.json"),
                       detect_silences(src, 0.25), info["dur"], not a.no_recheck)
        raw = d["words"]
        for w in snap_words(raw, segs, drops):
            nw = dict(w, s=remap(w["s"], segs, a.speed), e=remap(w["e"], segs, a.speed), norm=norm_word(w["w"]))
            if nw["e"] > nw["s"]:
                words.append(nw)
        print("   слов: %d" % len(words))
        for c in d.get("changes", []):
            print("   переслушано и исправлено %s" % c)
        for s, e in wordless_speech(sil, raw, info["dur"]):
            if not any(ds <= s and e <= de for ds, de in drops):
                warn.append("звук без слов на %.2f–%.2f с исходника (вздох, оговорка или потерянная фраза): "
                            "послушайте; лишнее убирается флагом --drop %.2f-%.2f" % (s, e, s - 0.1, e + 0.1))
    else:
        print("   пропущено")
    if info["audio"]:
        warn += check_cuts(envelope(wav), segs, drops)
        print("   склейки по звуку: %d, послушать мест: %d" % (len(segs) - 1, len(warn)))
        for x in warn:
            print("   ! " + x)

    print("3. лицо и запас кадра")
    ax, ay, zmax, how = face_anchor(src)
    print("   глаза x=%.2f y=%.2f (%s), предельная крупность %.2f" % (ax, ay, how, zmax))
    if a.frame:
        global W, H
        W, H = FRAME["w"], FRAME["h"]
        if not a.dry_run:
            framed = os.path.join(work, "tight_frame.mp4")
            precrop_to_window(tight, ay, framed)
            tight = framed
            ax, ay, zmax, how = face_anchor(tight, at=1.0)
            print("   в окне 4:5: глаза x=%.2f y=%.2f, предельная крупность %.2f" % (ax, ay, zmax))
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
    put_brolls(v_shots, [parse_broll(b) for b in a.broll], v_broll, a.broll_speed)

    flashes = []
    if a.flash is not None:
        flashes = a.flash or pick_flashes(shots)
    if a.lut or flashes or a.frame:
        print("   вид:%s%s%s" % (" цвет" if a.lut else "", " засветы на %s с" % ", ".join("%.1f" % t for t in flashes) if flashes else "",
                               " рамка" if a.frame else ""))
    v_look = os.path.join(work, "v_look.mp4")
    apply_look(v_broll, v_look, work, a.lut and os.path.abspath(a.lut), a.lut_mix, flashes, a.frame)

    print("7. титры")
    v_subs = v_look
    hits, bands, faces = [], [], []
    if words:
        faces = scan_faces(v_look)
        ass = os.path.join(work, "subs.ass")
        if a.subs == "plate":
            # плашка встаёт под подбородок: по замеру лица, а не на глаз
            chins = sorted(f[4] for f in faces)
            low, high = (1250, 1440) if not a.frame else (1250, (CH + FRAME["h"]) // 2 - 150)
            top = int(min(high, max(low, chins[int(len(chins) * 0.95)] + 44))) if chins else 1320
            bands = gen_plate(words, ass, a.font, a.font_bold, a.cta_colour, top, a.frame)
            print("   плашка на высоте %d" % top)
        else:
            hits, bands = gen_ass(words, accent, cta, ass, a.font, a.font_bold, a.cta_colour, a.frame)
    cover = None
    if not a.no_cover:
        cover = os.path.join(work, "cover.jpg")
        seams = [round(remap(e, segs, a.speed), 2) for s, e in segs[:-1]]
        t, cand = pick_cover(v_look, seams, cover, a.cover_at, os.path.join(work, "cover-sheet.png"))
        print("   обложка: кадр на %.2f с (кандидаты: %s)" % (t, ", ".join("%.2f" % c for c in cand)))
    if words or cover:
        v_subs = os.path.join(work, "v_subs.mp4")
        ins, chain = ["-i", v_look], "[0:v]%sformat=yuv420p[v]" % ("subtitles=subs.ass," if words else "")
        if cover:
            # обложка заменяет нулевой кадр, а не добавляется: длина и синхрон не меняются
            ins += ["-i", cover]
            chain = "[0:v]%snull[s];[1:v]scale=%d:%d[c];[s][c]overlay=enable='eq(n,0)',format=yuv420p[v]" % (
                "subtitles=subs.ass," if words else "", CW, CH)
        # у фильтра subtitles путь с двоеточием диска ломается, поэтому запуск из рабочей папки
        run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", chain, "-map", "[v]", "-map", "0:a?",
             "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-c:a", "copy", v_subs], cwd=work)

    print("8. звук")
    sfx = []
    if a.whoosh:
        sfx += [(a.whoosh, sh["s"], "0.45") for sh in shots if sh["move"] in ("punch", "pullout")]
        sfx += [(a.whoosh, max(0.0, t - 0.1), "0.30") for t in flashes]
    if a.pop:
        sfx += [(a.pop, w["s"], "0.30") for w in hits]
    auto = thin_sfx(sfx)
    if len(auto) < len(sfx):
        print("   звуков-акцентов %d, оставлено %d (не чаще раза в 2 с)" % (len(sfx), len(auto)))
    failed = []
    if a.no_master:
        mix_audio(v_subs, tight, a.music, auto + [parse_sfx(x) for x in a.sfx], out)
    else:
        mixed = os.path.join(work, "mixed.mp4")
        mix_audio(v_subs, tight, a.music, auto + [parse_sfx(x) for x in a.sfx], mixed)
        was, lufs, peak, ok = master(mixed, out, a.lufs, cover)
        print("   громкость: было %.1f, стало %s LUFS, пик %s дБ — %s" % (was, lufs, peak, "ок" if ok else "МИМО ЦЕЛИ"))
        if not ok:
            failed.append("громкость не попала в %.0f ±1 LUFS" % a.lufs)
    if cover:
        shutil.copy(cover, os.path.splitext(out)[0] + "-cover.jpg")

    print("9. проверка готового ролика")
    if bands and faces:
        hit = face_overlaps(faces, bands)
        print("   текст на лице: %s" % ("нет" if not hit else ", ".join(
            "%.1f с" % s if s == e else "%.1f–%.1f с" % (s, e) for s, e in hit)))
        if hit:
            failed.append("титры заходят на лицо в %d местах" % len(hit))
    elif bands:
        print("   лицо не найдено, проверьте титры по раскадровке")
    if warn:
        print("   послушать перед показом: %d мест (список в шаге 2)" % len(warn))

    sheet = os.path.splitext(out)[0] + "-sheet.png"
    contact_sheet(out, sheet)
    print("\nготово: %s  (%.1f с)" % (out, probe(out)["dur"]))
    print("раскадровка: %s — посмотрите её прежде чем открывать ролик" % sheet)
    if failed:
        print("\nНЕ ПРОШЛО ПРОВЕРКУ, показывать человеку рано:")
        for x in failed:
            print("  - " + x)
        sys.exit(2)


if __name__ == "__main__":
    main()
