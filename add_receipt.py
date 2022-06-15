import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

import receipt_parser as rp


def parse_opts():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-i",
        "--input",
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
        "-o",
        "--output",
        type=lambda p: Path(p).absolute(),
        default=Path(".").absolute(),
        help="Path to the output directory",
    )

    return parser.parse_args()


def get_receipt_timestamp(filename):
    with open(filename) as f:
        result = rp.parse_receipt(json.load(f))
        return str(int(datetime.timestamp(result["date"])))


def copy_file(from_, to):
    ts = get_receipt_timestamp(from_)
    checksum = file_checksum(from_)
    new_path = to / f"receipt_{ts}_{checksum}.json"
    shutil.copy(from_, new_path)


def copy_directory(from_, to):
    for p in Path(from_).glob(pattern="*.json"):
        copy_file(p, to)


def file_checksum(filename):
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def main():

    opts = parse_opts()

    if opts.dir:
        copy_directory(opts.dir, opts.output)
    else:
        copy_file(opts.input, opts.output)


if __name__ == "__main__":
    main()
