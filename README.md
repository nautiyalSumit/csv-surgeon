# csv-surgeon

✂️ A simple CLI tool to split, merge, and filter CSV files.

---

## Features

- **Split** large CSV files into smaller chunks.
- **Merge** multiple CSV files into one.
- **Filter** rows by column values.
- Easy-to-use CLI with `--help` for guidance.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nautiyalSumit/csv-surgeon.git
cd csv-surgeon
```

Install with Poetry:

```bash
poetry install
```

Run locally:

```bash
poetry run csv-surgeon --help
```

---

## Usage

### Split a CSV file

```bash
poetry run csv-surgeon split data.csv -n 100 -p chunk
```

➡️ Splits `data.csv` into chunks of 100 rows each, prefixed with `chunk_`.

---

### Merge CSV files

```bash
poetry run csv-surgeon merge file1.csv file2.csv -o out.csv
```

➡️ Merges multiple CSV files into `out.csv`.

---

### Filter CSV rows

```bash
poetry run csv-surgeon filter data.csv -c status -v active -o active.csv
```

➡️ Filters rows from `data.csv` where column `status` has the value `active`, saving results to `active.csv`.

---

## Help

Show available commands and options:

```bash
poetry run csv-surgeon --help
```

---
## Demo

### Split
![Split CSV](assets/split.png)

### Merge
![Merge CSV](assets/merge.png)

### Filter
![Filter CSV](assets/filter.png)


## Development

Run tests with:

```bash
poetry run pytest -v
```

Lint and format with:

```bash
poetry run ruff check .
poetry run black .
poetry run mypy src
```

---

## Version

Current: **v0.1.0**

---

## License
MIT License © 2025 [Sumit Nautiyal](https://github.com/nautiyalSumit)