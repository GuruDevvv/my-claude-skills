# Контрольные страницы check.mjs

Прогон: `node ../check.mjs . --widths 390` из этой папки. Ожидаемо:

| Файл | Должно быть |
|---|---|
| bad-group-opacity.html | FAIL unreadable (≈2,85 — плашка и текст выцветают вместе) |
| good-alpha-panel.html | чисто (≈ 8,8; наивный подсчёт даёт ложные 1,26) |
| bad-low-contrast.html | FAIL unreadable |
| bad-overflow.html | FAIL horizontal scroll |
| bad-stuck-reveal.html | FAIL invisible after full scroll |
| good-clean.html | чисто |

Правишь check.mjs — прогони этот набор: все bad-* обязаны упасть, все good-* пройти.
