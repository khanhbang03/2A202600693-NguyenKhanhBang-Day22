#!/usr/bin/env python3
"""Train the creative-bonus DPO adapter using the main lab trainer.

Run after NB1 creates `adapters/sft-mini/`:
    python bonus/train.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREF = ROOT / "bonus" / "data" / "pairs.parquet"
OUT = ROOT / "bonus" / "adapters" / "dpo-python-tutor"


def main() -> int:
    if not PREF.exists():
        subprocess.check_call([sys.executable, str(ROOT / "bonus" / "data" / "generate_pairs.py")])
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "train_dpo.py"),
        "--pref-path",
        str(PREF),
        "--output-dir",
        str(OUT),
        "--beta",
        "0.1",
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
