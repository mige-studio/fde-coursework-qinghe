#!/bin/zsh
set -eu
cd -- "$(dirname -- "$0")"
exec .venv/bin/python tools/run_local.py product.py start --actions --port 65378
