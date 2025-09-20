"""CLI entry point for executing the morning briefing workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from assistant.morning import create_default_service


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the morning market briefing workflow.")
    parser.add_argument(
        "--export",
        type=Path,
        default=None,
        help="Optional path to export the generated briefing report.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("configs"),
        help="Directory containing connector configuration files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = create_default_service(str(args.config_dir))
    report = service.run()
    print(report)
    if args.export is not None:
        args.export.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
