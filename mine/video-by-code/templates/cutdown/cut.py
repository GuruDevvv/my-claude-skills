"""Нарезка: вертикальный ролик из кадров готового видео + тезисы поверх + синтезированный звук.

Например: кадры героя из исходника, кроваво-красный тон, зерно, мерцание, тезисы
проявляются на кадре, под ними гул и сердцебиение. Монтажки нет: всё
делает ffmpeg по фильтрам, которые собирает этот скрипт.

    python cut.py plan.json           -> out.mp4
    python cut.py plan.json --sheet   -> sheet.png (по кадру на сцену, без звука и склейки)

plan.json — список сцен и стиль (пример — plan.example.json):
    {"source": "input.mp4", "style": "horror", "scene_sec": 5,
     "scenes": [{"at": "00:01:20", "text": "Тезис", "accent": "красная строка"}, ...]}
  at     — с какой секунды исходника брать кадр (берётся отрезок длиной scene_sec);
  x      — необязательно: доля по ширине, где центр вертикального кадра (0..1, по умолчанию 0.5);
  text   — белая строка, accent — вторая, цветом стиля (на ней бьёт «удар» в звуке).

Нужны: Python 3.9+, ffmpeg в PATH. Сторонних пакетов нет.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

W, H, FPS = 1080, 1920, 30

STYLES = {
    # цвет: фильтры ffmpeg поверх кадра; accent — цвет второй строки (hex для drawtext)
    "horror": {
        "grade": ["hue=s=0", "eq=contrast=1.45:brightness=-0.06",
                  "colorchannelmixer=rr=1.25:gg=0.22:bb=0.18", "vignette=angle=PI/3.2"],
        # мерцание: яркость скачет по формуле от времени — «лампа барахлит»
        "flicker": "eq=eval=frame:brightness='-0.04*lt(mod(t*5.3\\,1)\\,0.12)'",
        "grain": 22, "accent": "0xff2a2a", "drone_hz": 55, "beat": True,
    },
    "clean": {
        "grade": ["eq=contrast=1.08:saturation=1.1", "vignette=angle=PI/5"],
        "flicker": None, "grain": 6, "accent": "0x3dd6f5", "drone_hz": 110, "beat": False,
    },
}


def find_font():
    """Жирный шрифт с кириллицей: свой путь — переменная FONT, иначе ищем системный."""
    if os.environ.get("FONT"):
        return os.environ["FONT"]
    for p in ("C:/Windows/Fonts/arialbd.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"):
        if os.path.isfile(p):
            return p
    sys.exit("Не нашёл жирный шрифт с кириллицей. Укажите путь: FONT=/путь/к/шрифту.ttf")


def ff_path(p):
    """Путь для фильтров ffmpeg: прямые слэши, двоеточие диска экранировано (Windows)."""
    return p.replace("\\", "/").replace(":", "\\:")


def run(args):
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args])
    if r.returncode:
        sys.exit("ffmpeg упал на: " + " ".join(args[:12]) + " …")


def probe_size(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", src],
                         capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def scene_filter(sc, style, font, tmp, i, sec, src_w, src_h):
    # 1) вырезаем вертикальный кадр 9:16 из горизонтального и растягиваем до 1080x1920
    cw = min(src_w, int(src_h * 9 / 16))
    cx = int(max(0, min(src_w - cw, sc.get("x", 0.5) * src_w - cw / 2)))
    vf = [f"crop={cw}:{src_h}:{cx}:0", f"scale={W}:{H}", f"fps={FPS}"]
    vf += style["grade"]
    if style["flicker"]:
        vf.append(style["flicker"])
    # 2) текст: строки пишем в файлы — так не нужно экранировать кавычки и двоеточия
    y = int(H * 0.62)
    for key, color, size, start in (("text", "white", 76, 0.4), ("accent", style["accent"], 68, 1.6)):
        if not sc.get(key):
            continue
        for line in textwrap.wrap(sc[key], 22):
            f = os.path.join(tmp, f"t{i}_{key}_{y}.txt")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(line)
            # проявление: прозрачность растёт от 0 до 1 за 0.5 с начиная с start
            vf.append(f"drawtext=fontfile='{ff_path(font)}':textfile='{ff_path(f)}':"
                      f"fontsize={size}:fontcolor={color}:x=(w-text_w)/2:y={y}:"
                      f"box=1:boxcolor=black@0.55:boxborderw=16:"   # плашка: текст читается на любом кадре
                      f"shadowcolor=black@0.8:shadowx=3:shadowy=3:"
                      f"alpha='clip((t-{start})/0.5\\,0\\,1)'")
            y += int(size * 1.25)
        y += 30
    vf.append(f"noise=alls={style['grain']}:allf=t")
    if i > 0:   # первую сцену не затемняем: её первый кадр станет обложкой в ленте
        vf.append("fade=in:st=0:d=0.3")
    vf += [f"fade=out:st={sec - 0.4}:d=0.4", "format=yuv420p"]
    return ",".join(vf)


def sound(plan, style, total, out):
    """Звук из формул: низкий гул (два близких синуса дают «биение»), коричневый шум
    за фильтром и, в стиле horror, сердцебиение «тук-тук» раз в секунду."""
    f0 = style["drone_hz"]
    expr = f"0.30*sin(2*PI*{f0}*t)+0.22*sin(2*PI*{f0 * 1.013:.3f}*t)+0.10*sin(2*PI*{f0 * 1.5:.1f}*t)"
    if style["beat"]:
        # удар = синус 50 Гц, гаснущий экспонентой; второй удар через 0.25 с — «тук-тук»
        expr += ("+0.9*sin(2*PI*50*t)*exp(-28*mod(t\\,1))"
                 "+0.6*sin(2*PI*48*t)*exp(-28*mod(t-0.25\\,1))*gte(t\\,0.25)")
    run(["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={total}",
         "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.25:d={total}:r=48000",
         "-filter_complex", "[1]lowpass=f=300[n];[0][n]amix=inputs=2:normalize=0,"
         f"afade=in:d=1,afade=out:st={total - 1.5}:d=1.5,"
         "loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[a]", "-ar", "48000", "-ac", "2", out])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    plan_path = os.path.abspath(sys.argv[1])
    here = os.path.dirname(plan_path)
    plan = json.load(open(plan_path, encoding="utf-8"))
    style = STYLES[plan.get("style", "horror")]
    sec = float(plan.get("scene_sec", 5))
    src = os.path.join(here, plan["source"])
    if not shutil.which("ffmpeg"):
        sys.exit("Нет ffmpeg в PATH — поставьте его (см. SKILL.md, «Установка»).")
    font = find_font()
    src_w, src_h = probe_size(src)
    tmp = tempfile.mkdtemp(prefix="cut_")
    segs = []
    sheet = "--sheet" in sys.argv
    for i, sc in enumerate(plan["scenes"]):
        seg = os.path.join(tmp, f"s{i:02d}.mp4")
        vf = scene_filter(sc, style, font, tmp, i, sec, src_w, src_h)
        if sheet:   # один кадр из середины сцены — проверить глазами до долгой сборки
            run(["-ss", str(sc["at"]), "-t", str(sec), "-i", src, "-vf", vf,
                 "-ss", str(sec * 0.6), "-frames:v", "1", seg.replace(".mp4", ".png")])
        else:
            run(["-ss", str(sc["at"]), "-t", str(sec), "-i", src, "-vf", vf, "-an",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", seg])
        segs.append(seg)
        print(f"сцена {i + 1}/{len(plan['scenes'])}")
    if sheet:
        out = os.path.join(here, "sheet.png")
        pngs = [s.replace(".mp4", ".png") for s in segs]
        args = sum((["-i", p] for p in pngs), [])
        run([*args, "-filter_complex",
             "".join(f"[{k}]scale=270:-1[v{k}];" for k in range(len(pngs)))
             + "".join(f"[v{k}]" for k in range(len(pngs))) + f"hstack=inputs={len(pngs)}",
             "-frames:v", "1", out])
        print("Лист:", out)
        return
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w", encoding="utf-8") as fh:
        fh.writelines(f"file '{s.replace(chr(92), '/')}'\n" for s in segs)
    total = sec * len(segs)
    wav = os.path.join(tmp, "audio.wav")
    sound(plan, style, total, wav)
    out = os.path.join(here, plan.get("out", "out.mp4"))
    run(["-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Готово: {out} — {len(segs)} сцен, {total:.0f} с")


if __name__ == "__main__":
    main()
