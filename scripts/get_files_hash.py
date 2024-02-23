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
        file_paths = [sys.argv[1]]
    except IndexError as e:
        with open('airdrops/index_v1.json', 'r') as f:
            index = json.load(f)
        file_paths = [data['csv_path'] for data in index['airdrops'].values()]
        file_paths.extend([data[0] for data in index['poap_airdrops'].values()])

    for file_path in file_paths:
        with open(file_path, 'br') as f:
            print(hashlib.sha256(f.read()).hexdigest(), file_path)
