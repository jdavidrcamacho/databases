import json
import glob
import os

import pandas as pd  # type: ignore

# Get the current working directory
# directory_path = os.getcwd()
directory_path = '/home/camacho/GitLab/kypo-exploration/data'
exercise_directories = os.listdir(directory_path)

json_files = []
log_entries: list[dict[str, str]] = []

for i, folder in enumerate(exercise_directories):
    # print(f"\n{i+1} - {folder}")
    exercise_singles = os.listdir(f"{directory_path}/{folder}")
    for j, single in enumerate(exercise_singles):
        if single != "topology.yml":
            # print(f"{i+1}.{j+1} - {folder} from {single}")
            data_path = f"{directory_path}/{folder}/{single}/commands"
            for json_file in glob.glob(f"{data_path}/*.json"):
                # print(json_file)
                json_files.append(json_file)
                with open(json_file, "r") as file:
                    for entry in file:
                        log_entries.append(json.loads(entry))

# Relational
df = pd.DataFrame(log_entries)
df.to_parquet("src/data/FullData.parquet")
# Non-relational
with open("src/data/FullData.json", "w") as final:
    json.dump(log_entries, final)
