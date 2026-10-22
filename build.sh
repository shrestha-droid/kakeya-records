#!/bin/sh
# Regenerate every figure and document from results/*.json. Usage: ./build.sh [python]
set -e
PY=${1:-python3}
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MPLBACKEND=Agg $PY paper/make_figure.py
MPLBACKEND=Agg $PY video/make_assets.py
$PY paper/fill.py
perl -e "alarm 90; exec @ARGV" "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=paper/summary.pdf "file://$PWD/paper/summary.html" 2>/dev/null
