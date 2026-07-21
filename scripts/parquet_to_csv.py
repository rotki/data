#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "polars>=1.0",
# ]
# ///
"""Convert every Parquet file in a directory to a gzip-compressed CSV file."""

import argparse
import gzip
from pathlib import Path

import polars as pl


DEFAULT_AIRDROPS_DIR = Path(__file__).resolve().parent.parent / "airdrops"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=DEFAULT_AIRDROPS_DIR,
        help="directory containing Parquet files (default: repository airdrops directory)",
    )
    return parser.parse_args()


def convert_file(parquet_path: Path) -> Path:
    output_path = parquet_path.with_suffix(".csv.gz")
    temporary_path = output_path.with_suffix(f"{output_path.suffix}.tmp")

    try:
        dataframe = pl.read_parquet(parquet_path)
        with temporary_path.open(mode="wb") as temporary_file:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=temporary_file,
                mtime=0,
            ) as compressed_file:
                dataframe.write_csv(compressed_file)
        temporary_path.replace(output_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    return output_path


def main() -> None:
    directory = parse_args().directory.expanduser().resolve()
    if not directory.is_dir():
        raise SystemExit(f"Directory does not exist: {directory}")

    parquet_paths = sorted(directory.glob("*.parquet"))
    if not parquet_paths:
        raise SystemExit(f"No Parquet files found in: {directory}")

    for parquet_path in parquet_paths:
        output_path = convert_file(parquet_path)
        print(f"{parquet_path.name} -> {output_path.name}")


if __name__ == "__main__":
    main()
