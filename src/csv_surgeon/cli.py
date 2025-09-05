import argparse
import csv


def split_csv(file: str, rows: int, prefix: str) -> None:
    """Split a CSV into chunks with N rows each."""
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        chunk = []
        idx = 1
        for i, row in enumerate(reader, 1):
            chunk.append(row)
            if i % rows == 0:
                out_file = f"{prefix}_part{idx}.csv"
                with open(out_file, "w", newline="", encoding="utf-8") as out:
                    writer = csv.writer(out)
                    writer.writerow(header)
                    writer.writerows(chunk)
                chunk = []
                idx += 1
        if chunk:
            out_file = f"{prefix}_part{idx}.csv"
            with open(out_file, "w", newline="", encoding="utf-8") as out:
                writer = csv.writer(out)
                writer.writerow(header)
                writer.writerows(chunk)


def merge_csv(file1: str, file2: str, output: str) -> None:
    """Merge two CSV files (keeping header only once)."""
    with open(output, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        for i, f in enumerate([file1, file2]):
            with open(f, newline="", encoding="utf-8") as inp:
                reader = csv.reader(inp)
                header = next(reader)
                if i == 0:
                    writer.writerow(header)  # only first header
                for row in reader:
                    writer.writerow(row)


def filter_csv(input_file: str, output_file: str, column: str, value: str) -> None:
    """Filter rows where column == value and write to output CSV."""
    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            raise ValueError("Input CSV has no header row")

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get(column) == value:
                    writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        prog="csv-surgeon",
        description="Perform split, merge, and filter operations on CSV files.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # filter
    parser_filter = subparsers.add_parser("filter", help="Filter rows by column value")
    parser_filter.add_argument("file", help="CSV file")
    parser_filter.add_argument("column", help="Column name")
    parser_filter.add_argument("value", help="Value to match")
    parser_filter.add_argument("output", help="Output CSV file")
    parser_filter.set_defaults(
        func=lambda args: filter_csv(args.file, args.output, args.column, args.value)
    )

    # merge
    merge_parser = subparsers.add_parser("merge", help="Merge two CSV files")
    merge_parser.add_argument("file1")
    merge_parser.add_argument("file2")
    merge_parser.add_argument(
        "-o", "--output", default="output.csv", help="Output CSV file"
    )
    merge_parser.set_defaults(
        func=lambda args: merge_csv(args.file1, args.file2, args.output)
    )

    # split
    split_parser = subparsers.add_parser("split", help="Split a CSV into parts")
    split_parser.add_argument("file")
    split_parser.add_argument("-n", "--rows", type=int, required=True)
    split_parser.add_argument("-p", "--prefix", default="chunk")
    split_parser.set_defaults(
        func=lambda args: split_csv(args.file, args.rows, args.prefix)
    )

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
