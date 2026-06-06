#!/usr/bin/env bash
# Сборка PDF из markdown-источника гида
# Использование: ./build-pdf.sh [имя-файла-без-расширения]

set -euo pipefail

cd "$(dirname "$0")"

SRC="${1:-llm-benchmarks-guide-2026}"
INPUT="${SRC}.md"
HTML="${SRC}.html"
PDF="${SRC}.pdf"
CSS="guide-style.css"

if [ ! -f "$INPUT" ]; then
  echo "Источник не найден: $INPUT"
  exit 1
fi

if [ ! -f "$CSS" ]; then
  echo "CSS не найден: $CSS"
  exit 1
fi

# 1. Markdown → HTML (через pandoc)
# Используем gfm (GitHub-flavored), чтобы корректно обрабатывались таблицы.
echo "[1/2] Markdown → HTML"
pandoc "$INPUT" \
  --from=markdown+raw_html+yaml_metadata_block \
  --to=html5 \
  --standalone \
  --css="$CSS" \
  --metadata=lang=ru \
  --variable=title="" \
  --variable=subtitle="" \
  --variable=author="" \
  --variable=date="" \
  --output="$HTML"

# 2. HTML → PDF (через weasyprint, отличная поддержка кириллицы и CSS)
echo "[2/2] HTML → PDF"
weasyprint "$HTML" "$PDF"

# 3. Уборка промежуточного HTML (опционально)
# rm "$HTML"

echo ""
echo "Готово: $(pwd)/$PDF"
ls -lh "$PDF"
