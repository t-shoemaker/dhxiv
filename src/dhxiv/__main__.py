#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
from pathlib import Path

from .harvest import harvest_records

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger(__name__)


def main(argv=None):
    """Run the script."""
    parser = argparse.ArgumentParser("Harvest paper metadata from arXiv")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        metavar="DIR",
        help="Output directory for JSONL shards",
    )
    parser.add_argument(
        "-y",
        "--years",
        type=int,
        default=5,
        metavar="YEARS",
        help="Years back to harvest",
    )
    parser.add_argument(
        "-f",
        "--field",
        choices=["cs", "math", "stat"],
        default="cs",
        metavar="FIELD",
        help="arXiv field identifier",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=10_000,
        metavar="N",
        help="Records per shard",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="records",
        metavar="PREFIX",
        help="Prefix for shard filenames",
    )
    args = parser.parse_args()

    if args.years <= 0:
        parser.error("Years must be positive")

    if args.size <= 0:
        parser.error("Shard size must be positive")

    if args.output.exists() and not args.output.is_dir():
        parser.error(
            f"Output path exists but is not a directory: {args.output}"
        )

    harvest_records(
        args.output, args.years, args.field, args.size, args.prefix
    )


if __name__ == "__main__":
    main()
