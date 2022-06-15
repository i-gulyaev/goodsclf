import argparse
import csv
import json
from pathlib import Path

import receipt_parser as rp


def parse_opts():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-f",
        "--file",
        type=lambda p: Path(p).absolute(),
        help="path to the input file",
    )

    group.add_argument(
        "-d",
        "--dir",
        type=lambda p: Path(p).absolute(),
        help="input directory",
    )

    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="add new data to the output data file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=lambda p: Path(p).absolute(),
        help="Path to the output file",
        required=True,
    )

    return parser.parse_args()


def make_rows(filename):
    with open(filename) as f:
        receipt = rp.parse_receipt(json.load(f))
        for item in receipt["items"]:
            row = {
                "date": receipt["date"],
                "seller": receipt["seller"],
                "total_sum": receipt["sum"],
                "item_name": item["name"],
                "item_price": item["price"],
                "item_quantity": item["quantity"],
                "item_sum": item["sum"],
            }
            yield row


def main():
    opts = parse_opts()

    mode = "w"
    if opts.add:
        mode = "a+"

    with open(opts.output, mode, newline="") as csvfile:
        fieldnames = [
            "date",
            "seller",
            "total_sum",
            "item_name",
            "item_price",
            "item_quantity",
            "item_sum",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not opts.add:
            writer.writeheader()

        if opts.dir:
            for p in Path(opts.dir).glob(pattern="*.json"):
                for row in make_rows(p):
                    writer.writerow(row)
        else:
            for row in make_rows(opts.file):
                writer.writerow(row)


if __name__ == "__main__":
    main()
