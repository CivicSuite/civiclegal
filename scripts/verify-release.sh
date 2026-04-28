#!/usr/bin/env bash
set -euo pipefail
echo "VERIFY-RELEASE: CivicLegal v0.1.1"
PYTHON_CANDIDATES=(); [[ -n "${CIVICLEGAL_RELEASE_PYTHON:-}" ]] && PYTHON_CANDIDATES+=("$CIVICLEGAL_RELEASE_PYTHON")
PYTHON_CANDIDATES+=(python python3 py "/mnt/c/Users/scott/AppData/Local/Microsoft/WindowsApps/python.exe")
PYTHON_BIN=""
for candidate in "${PYTHON_CANDIDATES[@]}"; do if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import build, pytest, ruff" >/dev/null 2>&1; then PYTHON_BIN="$candidate"; break; fi; done
if [[ -z "$PYTHON_BIN" ]]; then echo "[FAIL] python: no interpreter with build, pytest, and ruff available"; exit 1; fi
echo "[INFO] python: $PYTHON_BIN"
bash scripts/verify-docs.sh
"$PYTHON_BIN" scripts/check-civiccore-placeholder-imports.py
"$PYTHON_BIN" -m pytest -q
"$PYTHON_BIN" -m ruff check .
rm -rf dist
"$PYTHON_BIN" -m build
"$PYTHON_BIN" - <<'PY'
from pathlib import Path
import hashlib
expected={"civiclegal-0.1.1-py3-none-any.whl","civiclegal-0.1.1.tar.gz"}
dist=Path("dist"); found={p.name for p in dist.iterdir() if p.is_file()}; missing=expected-found
if missing: raise SystemExit(f"missing artifacts: {sorted(missing)}")
lines=[]
for name in sorted(expected): lines.append(f"{hashlib.sha256((dist/name).read_bytes()).hexdigest()}  {name}")
(dist/"SHA256SUMS.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("[PASS] build artifacts and SHA256SUMS")
PY
"$PYTHON_BIN" - <<'PY'
import civiclegal
assert civiclegal.__version__ == "0.1.1"
print("[PASS] package version 0.1.1")
PY
echo "VERIFY-RELEASE: PASSED"
