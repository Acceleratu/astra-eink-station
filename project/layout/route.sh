#!/bin/sh
# Recreate the released board from the saved electrical block models and full
# routed session, and rerun the checks tied to its actual native copper.
set -eu
cd "$(dirname "$0")/.."
: "${PYTHON:=python3}"
"$PYTHON" tools/pcb_placement.py
"$PYTHON" tools/pcb_route.py dsn
"$PYTHON" tools/pcb_route.py ses
"$PYTHON" tools/pcb_board.py
"$PYTHON" tools/pcb_check.py
"$PYTHON" tools/pcb_returns.py
"$PYTHON" tools/pcb_resistance.py
