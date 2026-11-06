# Technical Redraw

[English](#english) · [Русский](#русский)

## English

An [Agent Skill](https://agentskills.io/specification) that turns a sketch or a part description into a clean black-and-white PNG with dimensions. If you don't specify a view, the agent asks before drawing.

Put the whole `technical-redraw` folder in your harness's skills directory. If skills aren't loaded automatically, give the agent the path to [`SKILL.md`](SKILL.md) and access to the whole folder. Rendering requires Python 3 with Pillow.

> Use technical-redraw to redraw the attached sketch in top view. Keep the given dimensions.

## Русский

Навык в формате [Agent Skills](https://agentskills.io/specification): превращает эскиз или описание детали в чёрно-белый PNG с размерами. Если вид не указан, агент уточнит его перед отрисовкой.

Поместите папку `technical-redraw` целиком в каталог навыков вашего харнесса. Если навыки не загружаются автоматически, укажите агенту путь к [`SKILL.md`](SKILL.md) и дайте доступ ко всей папке. Для отрисовки нужен Python 3 с Pillow.

> Используй technical-redraw: перечерти приложенный эскиз, вид сверху. Сохрани указанные размеры.

## Example / Пример

![Dimensioned drawings of a cup, rack, and scoop / Стакан, стеллаж и совок с размерами](example.png)

```sh
python -m pip install Pillow
python scripts/drawing.py --demo cup-preview.png
```
