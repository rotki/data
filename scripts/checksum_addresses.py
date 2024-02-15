import csv
import sys
from eth_utils import to_checksum_address


if __name__ == '__main__':
    data = []

    try:
        csv_path = sys.argv[1]
    except IndexError as e:
        raise ValueError('Please provide a csv file path') from e

    with open(csv_path) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader:
            data.append((to_checksum_address(row['address']), row['amount']))

    with open(csv_path, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['address', 'amount'])
        writer.writerows(data)
