from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("не X, а Y / не X — а Y", re.compile(r"\bне\s+[^.!?\n]{1,80}?\s*(?:,\s*а\s+|—\s*а\s+|-\s*а\s+)[^.!?\n]{1,120}", re.IGNORECASE)),
    ("звучит просто / на практике", re.compile(r"звучит\s+прост|на\s+практике\s+.{0,40}(сложн|трудн)", re.IGNORECASE)),
    ("важно отметить / стоит подчеркнуть", re.compile(r"важно\s+отметить|стоит\s+подчеркнуть|следует\s+учитывать|необходимо\s+отметить", re.IGNORECASE)),
    ("кроме того / более того / тем не менее", re.compile(r"кроме\s+того|более\s+того|тем\s+не\s+менее|в\s+заключение", re.IGNORECASE)),
    ("в мире где / в современном мире", re.compile(r"в\s+мире,\s+где|в\s+современном\s+мире|в\s+эпоху", re.IGNORECASE)),
    ("данный / является", re.compile(r"\bданн(?:ый|ая|ое|ые|ого|ому|ым|ых|ыми)\b|\bявляется\b", re.IGNORECASE)),
    ("ложная аудитория: друзья/читатели", re.compile(r"\bдрузья\b|дорогие\s+читатели", re.IGNORECASE)),
    ("это не X это Y", re.compile(r"это\s+не\s+[^.!?\n]{1,40},\s*это\s+", re.IGNORECASE)),
    ("афоризм-открытка: X живёт в Y", re.compile(r"\b(?:стыд|страх|боль|сила|любовь|правда)\s+живёт\s+в\s+", re.IGNORECASE)),
    ("нейро-заход: есть такое ощущение", re.compile(r"есть\s+такое\s+ощущение", re.IGNORECASE)),
    ("не вопрос X / это вопрос Y", re.compile(r"не\s+вопрос\s+[^.!?\n]{1,40}\.\s*Это\s+вопрос\s+", re.IGNORECASE)),
    ("стаккато через запятую", re.compile(r"(?:^|\.\s+)[А-ЯЁA-Z][а-яёa-z]+,\s+[а-яёa-z]+,\s+[а-яёa-z]+\.", re.MULTILINE)),
]

NEGATIVE_SENTENCE = re.compile(r"^\s*Не\s+\S.{0,80}[.!?]?\s*$")
TRIPLE_LIST = re.compile(
    r"\b[а-яёa-z][а-яёa-z -]{2,30},\s+[а-яёa-z][а-яёa-z -]{2,30},?\s+и\s+[а-яёa-z][а-яёa-z -]{2,30}[.!?]",
    re.IGNORECASE,
)


def sentence_split(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def check(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []

    # Count dashes per section (split by ---) to support multi-post files
    sections = re.split(r"\n---\n", text)
    for sec_idx, section in enumerate(sections):
        dash_count = section.count("—")
        if dash_count > 4:
            findings.append(f"Section {sec_idx + 1}: длинных тире {dash_count}, лимит 4")

    for name, pattern in PATTERNS:
        for match in pattern.finditer(text):
            sample = " ".join(match.group(0).split())
            findings.append(f"L{line_no(text, match.start())}: {name}: {sample}")

    for match in TRIPLE_LIST.finditer(text):
        sample = " ".join(match.group(0).split())
        findings.append(f"L{line_no(text, match.start())}: возможная тройка: {sample}")

    sentences = sentence_split(text)
    for idx in range(len(sentences) - 2):
        chunk = sentences[idx : idx + 3]
        if all(NEGATIVE_SENTENCE.match(sentence) for sentence in chunk):
            findings.append(f"S{idx + 1}: отрицательная тройка: {' / '.join(chunk)}")

    if not findings:
        print(f"{path}: ok")
        return 0

    print(f"{path}: {len(findings)} finding(s)")
    for finding in findings:
        print(f"  - {finding}")
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python neurotext_check.py <file.md> [file2.md ...]")
        return 2

    exit_code = 0
    for arg in sys.argv[1:]:
        exit_code = max(exit_code, check(Path(arg)))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
