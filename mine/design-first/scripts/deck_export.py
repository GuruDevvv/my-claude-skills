"""Колода из assets/deck-template.html: снимки слайдов, PDF, лист «нарисовано | собрано».

Браузер ищется так же, как в check.mjs (переменная CHROME_PATH, потом обычные места
Chrome/Edge), поэтому команды работают и там, где `chrome` нет в PATH.

    python deck_export.py shots prototypes/deck.html prototypes/_check/        # s01.png … 1920×1080
    python deck_export.py shots prototypes/deck.html prototypes/_bg/ --notext  # фоны без текста
    python deck_export.py pdf   prototypes/deck.html prototypes/deck.pdf       # страница = слайд
    python deck_export.py sheet prototypes/slides/ prototypes/_check/ prototypes/_check/pairs.jpg

Номера слайдов берутся из data-n у .frame. Лист сравнения ставит рядом файлы с одинаковым
номером: s01.png из папки нарисованных и s01.png из папки снимков.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

CANDIDATES = [os.environ.get("CHROME_PATH"),
              "C:/Program Files/Google/Chrome/Application/chrome.exe",
              "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
              "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
              "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def chrome():
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("Chrome/Edge не найден — задай CHROME_PATH")


def run(args, out):
    """Chrome пишет в out; старый файл убирается заранее, чтобы «OK» значило новый результат."""
    out = Path(out)
    out.unlink(missing_ok=True)
    prof = tempfile.mkdtemp(prefix="deck-chrome-")
    try:
        r = subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--user-data-dir={prof}",
                            "--virtual-time-budget=6000", *args],
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=180)
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    if r.returncode != 0 or not out.exists() or out.stat().st_size == 0:
        err = r.stderr.decode(errors="replace").strip().splitlines()[-1:] or [""]
        sys.exit(f"Chrome не сделал {out} (код {r.returncode}) {err[0]}")


def slide_numbers(html):
    nums = re.findall(r'class="frame"[^>]*data-n="(\d+)"|data-n="(\d+)"[^>]*class="frame"',
                      Path(html).read_text(encoding="utf-8"))
    return [int(a or b) for a, b in nums]


def shots(html, out_dir, notext):
    url = Path(html).resolve().as_uri()
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    nums = slide_numbers(html)
    if not nums:
        sys.exit(f"в {html} нет слайдов (.frame с data-n)")
    for n in nums:
        f = out / f"s{n:02d}.png"
        run(["--window-size=1920,1080", f"--screenshot={f.resolve()}",
             f"{url}?only={n}" + ("&notext=1" if notext else "")], f)
        print("OK " + str(f))


def pdf(html, out_pdf):
    out = Path(out_pdf).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    run(["--no-pdf-header-footer", f"--print-to-pdf={out}", Path(html).resolve().as_uri()], out)
    try:
        import fitz
        d = fitz.open(out)
        print(f"OK {out} | страниц {len(d)} | слайдов в колоде {len(slide_numbers(html))}")
    except ImportError:
        print(f"OK {out} (страницы не посчитаны: нет pymupdf)")


def sheet(drawn_dir, built_dir, out_img):
    from PIL import Image, ImageDraw
    W, H, GAP = 800, 450, 16
    names = sorted(p.name for p in Path(built_dir).glob("s[0-9]*.png") if ".v" not in p.stem)
    if not names:
        sys.exit(f"в {built_dir} нет снимков s01.png …")
    s = Image.new("RGB", (W * 2 + GAP * 3, (H + GAP) * len(names) + GAP), (24, 23, 28))
    d = ImageDraw.Draw(s)
    for i, n in enumerate(names):
        y = GAP + i * (H + GAP)
        for j, folder in enumerate((drawn_dir, built_dir)):
            p = Path(folder) / n
            x = GAP + j * (W + GAP)
            if p.exists():
                s.paste(Image.open(p).convert("RGB").resize((W, H)), (x, y))
            else:
                d.rectangle([x, y, x + W, y + H], outline=(200, 60, 60), width=3)
            d.text((x + 8, y + 6), ("нарисовано " if j == 0 else "собрано ") + n, fill=(255, 210, 120))
    Path(out_img).parent.mkdir(parents=True, exist_ok=True)
    s.save(out_img, quality=85)
    print(f"OK {out_img} | пар {len(names)}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("shots"); a.add_argument("html"); a.add_argument("out_dir"); a.add_argument("--notext", action="store_true")
    b = sub.add_parser("pdf"); b.add_argument("html"); b.add_argument("out_pdf")
    c = sub.add_parser("sheet"); c.add_argument("drawn_dir"); c.add_argument("built_dir"); c.add_argument("out_img")
    x = ap.parse_args()
    if x.cmd == "shots":
        shots(x.html, x.out_dir, x.notext)
    elif x.cmd == "pdf":
        pdf(x.html, x.out_pdf)
    else:
        sheet(x.drawn_dir, x.built_dir, x.out_img)


if __name__ == "__main__":
    main()
