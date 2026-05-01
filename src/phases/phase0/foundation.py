from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def cmd_info() -> int:
    print("My_Project :: AI-powered restaurant recommendation system")
    print("Phase: 0 complete, Phase 1 ingestion scaffolded")
    print(f"Project root: {PROJECT_ROOT}")
    print("Available commands: info, doctor, phase1-ingest-smoke")
    return 0


def _check_path(path: Path) -> tuple[str, bool]:
    return (str(path.relative_to(PROJECT_ROOT)), path.exists())


def cmd_doctor() -> int:
    required_paths = [
        PROJECT_ROOT / "docs" / "projectquery.md",
        PROJECT_ROOT / "docs" / "phase-wise-architecture.md",
        PROJECT_ROOT / "docs" / "phase0-scope.md",
        PROJECT_ROOT / "docs" / "dataset-contract.md",
        PROJECT_ROOT / ".env.example",
    ]

    print("Running phase-0 doctor checks...")
    all_ok = True

    for path in required_paths:
        label, exists = _check_path(path)
        status = "OK" if exists else "MISSING"
        print(f"[{status}] {label}")
        all_ok = all_ok and exists

    api_key_present = bool(os.getenv("GROQ_API_KEY"))
    print(f"[{'OK' if api_key_present else 'WARN'}] GROQ_API_KEY set")

    if all_ok:
        print("Phase 0 foundation checks passed.")
        return 0

    print("Phase 0 foundation checks failed. Create missing files and retry.")
    return 1

