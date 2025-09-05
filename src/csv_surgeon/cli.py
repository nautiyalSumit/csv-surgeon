import argparse
import csv


def split_csv(file, rows, prefix):
    with open(file, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        chunk = []
        idx = 1
        for i, row in enumerate(reader, 1):
            chunk.append(row)
            if i % rows == 0:
                out_file = f"{prefix}_part{idx}.csv"
                with open(out_file, "w", newline="") as out:
                    writer = csv.writer(out)
                    writer.writerow(header)
                    writer.writerows(chunk)
                chunk = []
                idx += 1
        if chunk:
            out_file = f"{prefix}_part{idx}.csv"
            with open(out_file, "w", newline="") as out:
                writer = csv.writer(out)
                writer.writerow(header)
                writer.writerows(chunk)


def merge_csv(file1, file2, output):
    with open(output, "w", newline="") as out:
        writer = csv.writer(out)
        for i, f in enumerate([file1, file2]):
            with open(f, newline="") as inp:
                reader = csv.reader(inp)
                header = next(reader)
                if i == 0:
                    writer.writerow(header)  # only first header
                for row in reader:
                    writer.writerow(row)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # merge
    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("file1")
    merge_parser.add_argument("file2")
    merge_parser.add_argument("-o", "--output", default="output.csv")

    # split
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("file")
    split_parser.add_argument("-n", "--rows", type=int, required=True)
    split_parser.add_argument("-p", "--prefix", default="chunk")

    args = parser.parse_args()

    if args.command == "merge":
        merge_csv(args.file1, args.file2, args.output)
    elif args.command == "split":
        split_csv(args.file, args.rows, args.prefix)
    else:
        parser.print_help()
