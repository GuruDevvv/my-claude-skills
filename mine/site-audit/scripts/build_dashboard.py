"""Build the one-file HTML dashboard from audit.json and open it in the browser.

Usage:
  python build_dashboard.py AUDIT.json OUT.html [--no-open]

AUDIT.json follows the schema in references/report.md ("Dashboard data"). The screenshot path in it,
if any, is resized and embedded, so OUT.html is a single file that works offline (fonts aside)
and can be sent to someone as is.
"""
import argparse, base64, io, json, os, sys, webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "dashboard.html"
LEVELS = {"broken", "important", "minor", "ok"}

def validate(d):
    errs = []
    for k in ("site", "blocks"):
        if k not in d: errs.append(f"missing top-level key: {k}")
    if d.get("lang", "en") not in ("en", "ru"): errs.append("lang must be 'en' or 'ru'")
    ids = set()
    for i, b in enumerate(d.get("blocks", [])):
        where = f"blocks[{i}] ({b.get('id', '?')})"
        for k in ("id", "name", "score", "summary"):
            if k not in b: errs.append(f"{where}: missing {k}")
        if b.get("id") in ids: errs.append(f"{where}: duplicate id")
        ids.add(b.get("id"))
        s = b.get("score")
        if not isinstance(s, (int, float)) or not 1 <= s <= 10: errs.append(f"{where}: score must be 1..10, got {s!r}")
        for j, it in enumerate(b.get("items", [])):
            if it.get("level") not in LEVELS: errs.append(f"{where}.items[{j}]: level must be one of {sorted(LEVELS)}")
            if not it.get("text"): errs.append(f"{where}.items[{j}]: missing text")
            if it.get("level") in ("broken", "important") and not it.get("fix"): errs.append(f"{where}.items[{j}]: {it['level']} item needs a fix")
    if not d.get("blocks"): errs.append("blocks is empty")
    for k in d.get("kpis", []):
        if "title" not in k or "value" not in k: errs.append(f"kpi without title/value: {k}")
    return errs

def embed_image(path, base):
    p = Path(path)
    if not p.is_absolute(): p = (base / p).resolve()
    if not p.exists():
        print(f"warning: screenshot not found, card shown without it: {p}", file=sys.stderr); return None
    try:
        from PIL import Image
        im = Image.open(p).convert("RGB")
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)))
        im = im.crop((0, 0, im.width, min(im.height, round(im.width * 0.75))))  # the card shows the top of the page
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data"); ap.add_argument("out"); ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    src = Path(a.data).resolve()
    d = json.loads(src.read_text(encoding="utf-8"))
    errs = validate(d)
    if errs:
        print("audit.json is not valid:\n  " + "\n  ".join(errs), file=sys.stderr); sys.exit(1)
    if d.get("screenshot"): d["screenshot"] = embed_image(d["screenshot"], src.parent)
    payload = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")  # keep the JSON from closing the <script> tag
    html = TEMPLATE.read_text(encoding="utf-8").replace("__AUDIT_JSON__", payload)
    out = Path(a.out).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    n_items = sum(len(b.get("items", [])) for b in d["blocks"])
    print(f"ok: {out} ({len(d['blocks'])} sections, {n_items} findings, {out.stat().st_size // 1024} KB)")
    if not a.no_open:
        try:
            os.startfile(str(out))  # Windows: default browser
        except AttributeError:
            webbrowser.open(out.as_uri())

if __name__ == "__main__":
    main()
