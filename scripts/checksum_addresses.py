"""
Checksum the addresses present in the given CSV file.
If no file is given, it will take all the CSVs from airdrops/index_v1.json

Usage:
    python scripts/checksum_addresses.py <path_to_csv>
    python scripts/checksum_addresses.py
"""
import csv
import json
import sys
from eth_utils import to_checksum_address


if __name__ == '__main__':
    data = []

    try:
        csv_paths = [sys.argv[1]]
    except IndexError as e:
        with open('airdrops/index_v1.json', 'r') as f:
            csv_paths = [data['csv_path'] for data in json.load(f)['airdrops'].values()]

    for csv_path in csv_paths:
        with open(csv_path) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader:
                data.append((to_checksum_address(row['address']), row['amount']))

        with open(csv_path, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['address', 'amount'])
            writer.writerows(data)
