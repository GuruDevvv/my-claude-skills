# reels-console

A vertical reel cut from one static take, entirely in the console. No CapCut, no timeline.

## When to use

You filmed yourself talking to the camera from one fixed position and now need a reel out of it:
pauses gone, the picture changing every couple of seconds, captions burned in, music sitting under
the voice. Also for the single steps on their own — stripping silences, adding word-timed subtitles.

## What it does

Finds the pauses by sound and cuts them, keeping 0.18 s so speech does not sound chopped. Runs
speech recognition for word-level timing and burns three levels of captions: small base lines, two
to four accent words in large type, one call-to-action word in colour. Locates the face, works out
**how far you can push in before the crown of the head gets cut**, and slices the take into crop
levels with the eyes on the upper third. Adds slow push-ins, a pull-out before the finish, and a
punch zoom with real motion blur — rendered at 180 fps and averaged six frames into one, not a blur
filter. Overlays B-roll, ducks music under the voice with a sidechain compressor, and ends by
laying twelve frames into one contact sheet so the result can be checked at a glance.

```bash
python scripts/reel.py take.mp4 --dry-run        # the edit plan, nothing rendered
python scripts/reel.py take.mp4 -o reel.mp4 --accent first main result --cta subscribe
```

## Not for

Choosing the take, deciding which word carries the sentence, or writing the script — that stays with
the human, or with the model running the skill. It also does not shoot B-roll that was never filmed:
one take gives one angle, and the second angle has to exist.

## Needs

`ffmpeg` and `ffprobe` on PATH, plus `pip install openai-whisper opencv-python insightface
onnxruntime` for captions and face anchoring. Without them it still runs — no captions, crop from
the centre of the frame. A Cyrillic-capable font for captions (Arial and Arial Black by default).

## Honest about maturity

Written and tested in one evening, on two sources: a real 52-second phone take (vertical 4K, front
camera) and a synthetic bench with B-roll and music. Multiple faces in frame, horizontal video and
languages other than Russian are untested — whisper handles them, but the caption styling was tuned
for Cyrillic. Long recordings will be slow: whisper on a CPU is the bottleneck, not ffmpeg.

The one thing worth knowing before you shoot: on that real take the face filled 49.5% of the frame
width, so there was nowhere to push in and the main technique never engaged. Stand 1.5–2 m from the
camera. The script measures this and warns before rendering.

`references/recipes.md` has every technique as a standalone ffmpeg command, with measurements and
the traps — why `crop` cannot change size over time, how the motion blur is actually made, why
`amix` without `normalize=0` quietly eats the voice.

---

🇷🇺 Монтаж вертикального ролика из одного статичного дубля целиком в консоли: вырезает паузы,
нарезает съёмку с одной точки на планы разной крупности с привязкой к лицу, ставит наезды и ударный
наезд со смазом движения, кладёт перебивки, рисует титры трёх уровней из распознавания речи,
подкладывает музыку с автоприглушением. Что показать и какое слово главное — решает человек.
Приёмы взяты из разбора видео ilioshots «Как снять динамичный REELS на 1 кв. метре».
