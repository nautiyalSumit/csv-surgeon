import os
import csv
from csv_surgeon.cli import split_csv, merge_csv, filter_csv


def test_split_csv_creates_chunks(tmp_path):
    # Make a dummy csv
    path = tmp_path / "data.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        for i in range(1, 11):  # 10 rows
            writer.writerow([i, f"user{i}"])

    # Run split
    split_csv(str(path), 3, str(tmp_path / "chunk"))

    # Check output files
    files = sorted([f for f in os.listdir(tmp_path) if f.startswith("chunk_part")])
    assert len(files) == 4  # 10 rows → 4 chunks of size 3 (last one smaller)

    # Check that header exists in each file
    for f in files:
        with open(tmp_path / f) as inp:
            rows = list(csv.reader(inp))
            assert rows[0] == ["id", "name"]


def test_merge_csv_combines_files(tmp_path):
    file1 = tmp_path / "f1.csv"
    file2 = tmp_path / "f2.csv"
    out = tmp_path / "out.csv"

    # Make two csv files
    with open(file1, "w", newline="") as f1, open(file2, "w", newline="") as f2:
        writer1 = csv.writer(f1)
        writer1.writerow(["id", "name"])
        writer1.writerow([1, "Alice"])

        writer2 = csv.writer(f2)
        writer2.writerow(["id", "name"])
        writer2.writerow([2, "Bob"])

    # Call merge_csv
    merge_csv([file1, file2], out)

    # Verify merged content
    with open(out, newline="") as f:
        rows = list(csv.reader(f))

    assert rows == [
        ["id", "name"],
        ["1", "Alice"],
        ["2", "Bob"],
    ]


def test_filter_csv_creates_expected_output(tmp_path):
    file = tmp_path / "data.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        writer.writerow([1, "Alice"])
        writer.writerow([2, "Bob"])
        writer.writerow([3, "Alice"])

    out = tmp_path / "filtered.csv"
    filter_csv(str(file), "name", "Alice", str(out))

    with open(out) as f:
        rows = list(csv.reader(f))

    assert rows == [["id", "name"], ["1", "Alice"], ["3", "Alice"]]
