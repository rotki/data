"""
Transform data from https://github.com/gnosis/cow-token-allocation to extract the base amount
airdroped and make the addreses checksumed.
"""
import argparse
import csv
from pathlib import Path

from eth_utils import to_checksum_address


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog='cow',
        description=(
            'Make sure that address are checksumed and amounts are only the base airdrop for cow',
        ),
    )
    p.add_argument(
        '--file',
        type=str,
        help='The file with the information for the airdrop',
        required=True,
    )
    p.add_argument(
        '--output',
        type=str,
        help='Name for the output file',
        required=True,
    )
    return p.parse_args()


def handle_file(input: Path, output: Path) -> None:
    new_rows = []
    with open(input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            address = to_checksum_address(row['Account'])
            amount = row['Airdrop']
            new_rows.append((address, amount))

    with open(output, 'w') as output_file:
        headers = ['address', 'amount']
        writer = csv.writer(output_file, delimiter=',')
        writer.writerow(headers)
        writer.writerows(new_rows)


if __name__ == '__main__':
    args = parse_args()
    input_file = Path(args.file)
    target_file = Path(args.output)
    handle_file(input_file, target_file)