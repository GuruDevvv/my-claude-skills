# HANDOFF — my-claude-skills
Обновлено: 2026-06-24 19:15

## Статус: 🟢 design-first v4 — добавлена фаза Feel pass

## Текущее состояние
design-first v4 (`369d94f`): добавлена финальная фаза **Feel pass** (Step 5.5) — полировка реального билда по 16 микро-правилам (дистиллят скилла `jakubkrehel/make-interfaces-feel-better`, MIT, кредит в README). Новый `references/feel-polish.md`. Запускается по умолчанию, скип «skip polish», НЕ применяется к прототипам. Прошло REVIEW через skill-conductor (production-ready). installed == repo. Обкатано на Olympics (см. ниже).

## Задачи
- Боевой прогон Feel pass на портированном дашборде Olympics («дорожки») | там зайдут концентрические радиусы + тени-вместо-границ, отложенные на легаси
- deep-research скилл всё ещё не ревьюился | свежий взгляд
- Прогнать skill-scanner на скиллах | безопасность

## Блокеры
Нет блокеров

## Хрупкие места
- Скилл грузится при СТАРТЕ Claude Code — после правки рестарт. installed-копия должна = repo (см. feedback_sync_installed_skill_after_edit).
- Валидатор skill-conductor строго парсит YAML → спотыкается на `Use when:` в description (пре-существующее, Claude Code грузит ОК). README внутри скилла — намеренная конвенция репо.

## Следующий шаг
Дождаться портирования дашборда Olympics на «дорожки» → повторный Feel pass (покажет отложенные принципы). Либо ревью deep-research.

## Промпт
> Проект my-claude-skills. Прочитай HANDOFF.md.
> design-first довели до v4: добавлена фаза Feel pass (Step 5.5 + references/feel-polish.md) — полировка финального билда по 16 микро-правилам Крехеля. Обкатано на Olympics (feel-pass в ветке redesign/site).
> Продолжи с: повторный Feel pass после портирования дашборда Olympics на «дорожки» (там зайдут отложенные концентрические радиусы/тени), либо ревью deep-research скилла.
