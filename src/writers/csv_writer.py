import csv
from pathlib import Path


class CSVWriter:

    @staticmethod
    def write(
        rows: list[dict],
        fieldnames: list[str],
        output_file: str,
    ) -> None:

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()
            writer.writerows(rows)

        print(f"Saved {len(rows)} rows to {output_path}")