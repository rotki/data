"""
Convert the given CSV file into a Parquet file.

Usage:
    scripts/csv_to_parquet.py <path_to_csv>
"""
import sys
import polars
from pathlib import Path


if __name__ == '__main__':
    csv_path = Path(sys.argv[1])
    polars.read_csv(
        source=csv_path,
        infer_schema_length=0
    ).write_parquet(csv_path.parent / f'{csv_path.stem}.parquet')
