import json
import glob

import pandas as pd  # type: ignore

directory_path = "src/data/sandbox"
log_entries: list[dict[str, str]] = []

for json_file in glob.glob(f"{directory_path}/*.json"):
    print(json_file)
    with open(json_file, "r") as file:
        for entry in file:
            log_entries.append(json.loads(entry))

df = pd.DataFrame(log_entries)
print(df)
df.to_parquet("src/data/sandbox.parquet")
