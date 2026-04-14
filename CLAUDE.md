# my-claude-skills

## О проекте
Коллекция кастомных скиллов для Claude Code. Публикуется на GitHub (GuruDevvv/my-claude-skills).

## Структура
Каждый скилл — папка с `SKILL.md`:
- `spec-first/` — структурированный запуск проекта (Vision → Blueprint)
- `design-first/` — генерация 4-6 HTML-прототипов дизайна
- `multi-layer-review/` — мульти-ревью спеки 5 параллельными агентами
- `project-audit/` — аудит организации проекта
- `deep-research/` — структурированное исследование с рейтингами уверенности

## Исследования
- `research/spec-first-research.md` — полное исследование Spec-First методологии
- `research/project-audit-prompt.txt` — шаблон промпта для аудита проекта

## Установка скилла
Скопировать папку в `~/.claude/skills/<skill-name>/` и перезапустить Claude Code.

## Разработка
Для создания/редактирования скиллов использовать `/skill-conductor` или `/skill-create`.
