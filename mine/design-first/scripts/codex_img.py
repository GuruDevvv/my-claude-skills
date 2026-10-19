"""Экономная генерация картинки через Codex (подписка Plus, gpt-image-2).

Обычный `codex exec` на картинку тянет ~43 тыс. токенов обвязки (AGENTS.md, список
навыков, MCP, хуки памяти), читает файлы и опрашивает «готово?» по 10 раз — замер
16.10.2026: 150 тыс. – 1,3 млн токенов на одну картинку. Здесь Codex запускается
голым: без config.toml, без AGENTS.md, без плагинов и хуков, с дешёвой моделью-
диспетчером. Рисует всё равно gpt-image-2, модель только вызывает инструмент.

Одновременно работают не больше MAX_SLOTS запусков, остальные ждут очереди.

    python codex_img.py "описание" out.png [--ref a.png --ref b.png] [--model gpt-6.1-sol] [--replace]

Файл out уже есть — отказ, чтобы не затереть чужую картинку. Перерисовка той же картинки —
с --replace: после удачной генерации старый файл переезжает в out.v1.png (v2, v3…).
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
SLOTS_DIR = CODEX_HOME / "tmp" / "img-slots"
MAX_SLOTS = 4
DEFAULT_MODEL = "gpt-6-luna"
FALLBACK_MODEL = "gpt-6.1-sol"
DISABLE = ["plugins", "apps", "multi_agent", "browser_use", "browser_use_external",
           "computer_use", "hooks", "goals", "tool_suggest", "sleep_tool", "view_image",
           "in_app_browser", "realtime_conversation", "skill_mcp_dependency_install"]

INCLUDE_OFF = ["include_skills_usage_instructions", "include_plugin_usage_instructions",
               "include_apps_usage_instructions", "include_apps_instructions",
               "include_collaboration_mode_instructions", "include_permissions_instructions",
               "include_environment_context"]

PROMPT = """Call the built-in image generation tool exactly once.
Prompt for the image: {prompt}
{refs}Rules: do not read any files, do not open skill docs, do not run shell commands,
do not view or check the result, do not call any other tool. As soon as the tool
returns, reply with the single word DONE."""


def pid_alive(pid):
    try:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                             capture_output=True, text=True,
                             encoding="cp866", errors="replace").stdout
        return str(pid) in out
    except Exception:
        return True


def take_slot():
    SLOTS_DIR.mkdir(parents=True, exist_ok=True)
    waited = False
    while True:
        for i in range(MAX_SLOTS):
            p = SLOTS_DIR / f"slot{i}.lock"
            try:
                fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode()); os.close(fd)
                return p
            except FileExistsError:
                try:
                    if not pid_alive(int(p.read_text() or 0)):
                        p.unlink(missing_ok=True)
                except (ValueError, OSError):
                    pass
        if not waited:
            print(f"очередь: уже идут {MAX_SLOTS} картинки, жду…", file=sys.stderr); waited = True
        time.sleep(3)


def run(prompt, refs, model, workdir):
    ref_txt = ""
    if refs:
        ref_txt = ("Pass these files as reference images to the tool (referenced image paths), "
                   "without opening them yourself: " + ", ".join(str(Path(r).resolve()) for r in refs) + "\n")
    cmd = [shutil.which("codex") or "codex", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
           "--json", "-m", model, "-c", 'model_reasoning_effort="low"',
           "-c", "project_doc_max_bytes=0", "-C", str(workdir)]
    for key in INCLUDE_OFF:
        cmd += ["-c", f"{key}=false"]
    for f in DISABLE:
        cmd += ["--disable", f]
    # задание через stdin: codex на Windows — это .cmd, и cmd.exe режет аргумент на первом переводе строки
    cmd.append("-")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       input=PROMPT.format(prompt=prompt, refs=ref_txt), timeout=600)
    thread, usage, err = None, None, None
    for line in r.stdout.splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") == "thread.started":
            thread = o.get("thread_id")
        elif o.get("type") == "turn.completed":
            usage = o.get("usage")
        elif o.get("type") in ("error", "turn.failed"):
            err = o.get("message") or (o.get("error") or {}).get("message")
    return thread, usage, err or (r.stderr[-400:] if r.returncode else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt"); ap.add_argument("out")
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--replace", action="store_true", help="перерисовать: старый файл сохранить как .vN")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    missing = [r for r in a.ref if not Path(r).is_file()]
    if missing:   # иначе Codex молча рисует без образца, и стиль уезжает
        sys.exit("нет файла-образца: " + ", ".join(missing))
    if out.exists() and not a.replace:
        sys.exit(f"файл уже есть, не перезаписываю: {out} (перерисовать — ключ --replace)")
    slot = take_slot()
    try:
        workdir = Path(tempfile.mkdtemp(prefix="codex-img-"))
        models = [a.model] + ([FALLBACK_MODEL] if a.model == DEFAULT_MODEL else [])
        for m in models:
            thread, usage, err = run(a.prompt, a.ref, m, workdir)
            imgs = sorted((CODEX_HOME / "generated_images" / (thread or "-")).glob("*.png"),
                          key=lambda p: p.stat().st_mtime)
            if imgs:
                out.parent.mkdir(parents=True, exist_ok=True)
                if out.exists():   # --replace: прежняя версия остаётся рядом, только после удачи
                    n = 1
                    while out.with_name(f"{out.stem}.v{n}{out.suffix}").exists():
                        n += 1
                    out.rename(out.with_name(f"{out.stem}.v{n}{out.suffix}"))
                shutil.copy2(imgs[-1], out)
                u = usage or {}
                print(f"OK {out} | модель {m} | вход {u.get('input_tokens')} "
                      f"(из кэша {u.get('cached_input_tokens')}), выход {u.get('output_tokens')}")
                return
            print(f"[{m}] картинки нет: {err}", file=sys.stderr)
            if err and "usage limit" in err:
                break
        sys.exit(1)
    finally:
        slot.unlink(missing_ok=True)
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
