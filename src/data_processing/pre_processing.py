import json
import glob
from pathlib import Path

import pandas as pd  # type: ignore


def process_json_file(
    json_file: Path, log_entries: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Process a JSON file and append the data to the list.

    Args:
        json_file (Path): Path to the JSON file.
        log_entries (list[dict[str, str]]): List the data will be appended.

    Raises:
        Exception: Error decoding the JSON file.

    Returns:
        list[dict[str, str]]: List containing the data.
    """
    with open(json_file, "r") as file:
        for entry in file:
            try:
                log_entries.append(json.loads(entry))
            except json.JSONDecodeError as e:
                raise Exception(
                    f"Error decoding JSON in file {json_file}."
                    f"Line: {entry}."
                    f"Error: {e}"
                )

    return log_entries


def process_json_directory(directory_path: str) -> list[dict[str, str]]:
    """Process all JSON files in the specified directory.

    Args:
        directory_path (Path): Path to the directory containing JSON files.

    Returns:
        list[dict[str, str]]: List with data from all processed JSON files.
    """
    log_entries: list[dict[str, str]] = []
    for json_file in glob.glob(f"{directory_path}/*.json"):
        process_json_file(json_file, log_entries)  # type: ignore

    return log_entries


def process_data(directory_path: str) -> pd.DataFrame:
    """Process log data from a directory and return a cleaned DataFrame.

    Args:
        directory_path (str): Path to the directory containing the JSON data.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    log_entries = process_json_directory(directory_path=directory_path)
    df = pd.DataFrame(log_entries)
    return df


if __name__ == "__main__":
    dataset = process_data("sandbox")
    dataset.to_parquet("dataset.parquet")
