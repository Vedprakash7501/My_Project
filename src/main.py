"""Phase 0 runnable skeleton and diagnostics entrypoint."""

from __future__ import annotations

import argparse

from phases.phase0 import cmd_doctor, cmd_info
from phases.phase1.ingestion import load_restaurants


def cmd_phase1_ingest_smoke(source: str, limit: int, split: str) -> int:
    try:
        restaurants = load_restaurants(source=source, limit=limit, split=split)
    except Exception as exc:
        print(f"Phase 1 ingest-smoke failed: {exc}")
        return 1

    print(f"Phase 1 ingest-smoke :: source={source}, split={split}, count={len(restaurants)}")
    for item in restaurants[:5]:
        print(
            f"- {item.name} | {item.location} | rating={item.rating} | "
            f"cost_band={item.cost_band} | cuisines={', '.join(item.cuisines)}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project utility commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("info", help="Show project phase information")
    subparsers.add_parser("doctor", help="Run phase-0 setup checks")
    ingest_parser = subparsers.add_parser(
        "phase1-ingest-smoke", help="Run phase-1 ingestion smoke check"
    )
    ingest_parser.add_argument("--source", choices=["sample", "hf"], default="sample")
    ingest_parser.add_argument("--split", default="train")
    ingest_parser.add_argument("--limit", type=int, default=10)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "info":
        return cmd_info()
    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "phase1-ingest-smoke":
        return cmd_phase1_ingest_smoke(source=args.source, limit=args.limit, split=args.split)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

