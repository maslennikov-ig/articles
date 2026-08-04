#!/usr/bin/env python3
"""lint_ru — обёртка над smixs/humanizer-ru lint.py под русский лонгрид.

Апстрим не меняем: он детерминированный, покрыт 19 eval-сценариями, и любая
правка внутри него ломает это свойство. Обёртка только отбрасывает классы
находок, которые для наших площадок ложные, и пересчитывает вердикт.

    python3 lint_ru.py draft.md
    python3 lint_ru.py draft.md --all      # без фильтра, как в апстриме
    python3 lint_ru.py --self-test

Что отбрасывается и почему — см. IGNORED. Каждое исключение обосновано
измерением, а не вкусом; беспричинно расширять список нельзя.
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint as upstream  # noqa: E402
import re

# Правило апстрима -> почему оно у нас не применяется.
IGNORED = {
    "23 длинное тире": (
        "В русском тире часто обязательно грамматически («Хабр — это сообщество»). "
        "Частота тире у автора 4.6 на 1000 знаков совпадает с нормой корпуса, "
        "то есть это не AI-маркер, а общая норма. Частоту проверяет "
        "voice_audit.py (dash_per_1k). Апстрим ловит и «—», и «–», поэтому "
        "замена начертания его не обходит — и предлагать её нельзя."
    ),
    "34 разделитель в теле": (
        "«---» в теле статьи — обязательный элемент структуры habr-article "
        "(разделитель после TL;DR и между блоками), а не склейка абзацев."
    ),
}



# --- локальные правила поверх апстрима ---------------------------------------
# Апстримовое «13 негативный параллелизм» ловит только форму с отрицанием
# впереди: «не просто X, а Y», «не только X, но и Y». Форму с утверждением
# впереди — «X, а не Y» — не ловит никто, а ИИ тянется именно к ней.
# Правило автора от 04.08.2026: такие хвосты минимизировать. Проверка простая —
# выкинуть вторую часть; если смысл не пострадал, её и не должно быть.
LOCAL_RULES = [
    ("13b хвост-противопоставление", re.compile(
        r"[^.!?\n]{10,90},\s+(?:а|но) не\s+(?!вышло|получилось|сработало|удалось|пришлось)[^.!?\n]{2,60}")),
]
# Форма живая и иногда несущая, поэтому это WARN, а не ERROR: гейт не роняет,
# но заставляет пройтись по списку и оставить только те, где контраст работает.
LOCAL_LEVEL = "WARN"


def local_findings(text):
    out = []
    for rule, rx in LOCAL_RULES:
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            out.append((LOCAL_LEVEL, line_no, rule, m.group(0).strip()[:90]))
    return out


def filtered(findings):
    keep, dropped = [], []
    for f in findings:
        (dropped if f[2] in IGNORED else keep).append(f)
    return keep, dropped


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    show_all = "--all" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    text = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()

    findings = upstream.lint(text) + local_findings(text)
    keep, dropped = (findings, []) if show_all else filtered(findings)

    for kind, line_no, rule, ctx in keep:
        loc = f"строка {line_no}" if line_no else "текст"
        print(f"{kind} {loc}: [{rule}] {ctx}")

    errors = [f for f in keep if f[0] == "ERROR"]
    warnings = [f for f in keep if f[0] == "WARN"]
    score, v = upstream.verdict(len(errors), len(warnings))
    print(f"\nитого: {len(errors)} errors, {len(warnings)} warnings, severity {score} -> {v}")

    if dropped:
        print(f"\nотфильтровано находок: {len(dropped)}")
        for rule in sorted({f[2] for f in dropped}):
            n = sum(1 for f in dropped if f[2] == rule)
            print(f"  [{rule}] x{n}")
            print(f"      {IGNORED[rule]}")
        print("  показать всё: --all")

    if errors:
        print("\nГЕЙТ НЕ ПРОЙДЕН — это находки, а не правки. Чинит автор.")
        return 1
    print("\nгейт пройден: жёстких запретов нет.")
    return 0


def self_test() -> int:
    # тире и разделитель отфильтрованы...
    t = "Хабр — это сообщество.\n\n---\n\nВторой абзац про другое дело.\n"
    keep, dropped = filtered(upstream.lint(t) + local_findings(t))
    assert dropped, "тире/разделитель обязаны попасть в отфильтрованные"
    assert not [f for f in keep if f[2] in IGNORED]

    # ...а настоящие жёсткие запреты проходят фильтр насквозь
    bad = "Это не просто курс, это экосистема. Скорость > идеальности."
    keep_bad, _ = filtered(upstream.lint(bad))
    kinds = [f[2] for f in keep_bad if f[0] == "ERROR"]
    assert any("13" in k for k in kinds), kinds
    assert any("мат-знаки" in k for k in kinds), kinds

    # артефакты копипаста фильтр не трогает
    art = "Данные citeturn0search2 подтверждают вывод исследования."
    keep_art, _ = filtered(upstream.lint(art))
    assert [f for f in keep_art if f[0] == "ERROR"], upstream.lint(art)

    print("self-test: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
