import argparse
import sys


def merge_command(files: list[str]):
    # Stub: just print for now
    print(f"Merging CSV files: {', '.join(files)}")


def main():
    parser = argparse.ArgumentParser(
        prog="csv-surgeon",
        description="CSV Surgeon - perform operations on CSV files"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- merge command ---
    merge_parser = subparsers.add_parser(
        "merge", help="Merge multiple CSV files")
    merge_parser.add_argument(
        "files",
        nargs="+",
        help="Paths to CSV files to merge"
    )

    args = parser.parse_args()

    if args.command == "merge":
        merge_command(args.files)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
