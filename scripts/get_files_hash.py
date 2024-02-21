"""
Print the SHA256 hash of the given CSV or JSON file.
If no file is given, it will print for all the CSVs and JSONs from airdrops/index_v1.json

Usage:
    python scripts/get_files_hash.py <path_to_csv>
    python scripts/get_files_hash.py
"""
import hashlib
import json
import sys


if __name__ == '__main__':
    try:
        csv_paths = [sys.argv[1]]
    except IndexError as e:
        with open('airdrops/index_v1.json', 'r') as f:
            csv_paths = [data['csv_path'] for data in json.load(f)['airdrops'].values()]
            f.seek(0)
            json_paths = [data[0] for data in json.load(f)['poap_airdrops'].values()]

    for csv_path in csv_paths:
        with open(csv_path, 'br') as f:
            print(hashlib.sha256(f.read()).hexdigest(), csv_path)

    for json_path in json_paths:
        with open(json_path, 'br') as f:
            print(hashlib.sha256(f.read()).hexdigest(), json_path)
