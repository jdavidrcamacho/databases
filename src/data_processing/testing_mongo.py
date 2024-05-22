import pymongo
import json
import re
from bson import json_util
from pymongo import MongoClient


# Convert to strict JSON
def read_mongoextjson_file(filename):
    with open(filename, "r") as f:
        bsondata = f.read()  # Convert Mongo object(s) to regular strict JSON
        jsondata = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)',
                          r'{"$oid": "\1"}',
                          bsondata)
        # Description of Mongo ObjectId:
        data = json.loads(jsondata, object_hook=json_util.object_hook)
        return data


# Connect to MongoDB (with error handling)
try:
    client = MongoClient("localhost", 27017)  # type: ignore
except pymongo.errors.ConnectionFailure:
    print("Error: Could not connect to MongoDB server.")
    exit(1)

db = client["my_database"]
collection = db["my_collection"]
collection.drop()  # Drop the collection (deletes all documents)

# Load JSON data
filenames = ["sandbox-396.json", "sandbox-397.json", "sandbox-398.json",
             "sandbox-399.json", "sandbox-400.json", "sandbox-401.json"]

for filename in filenames:
    try:
        print(f"\nOpening src/data/sandbox/{filename}")
        log_entries: list[dict[str, str]] = []
        with open(f"src/data/{filename}", "r") as f:
            for entry in f:
                try:
                    log_entries.append(json.loads(entry))
                except json.JSONDecodeError as e:
                    raise Exception(f"Error decoding JSON {filename}: {e}")
            # print(log_entries)
            collection.insert_many(log_entries)
        # for document in data:
        #   collection.insert_one(document)
        print(f"Data loaded successfully from {filename}!")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
print("\nAll data loaded!")


# Find all documents in the collection
all_documents = collection.find()
num_entries = len(list(all_documents.clone()))
print(f"DB entries: {num_entries}")

# # Loop through each document and print it
# for document in all_documents:
#     print(document)

# # Find documents with specific criteria (filters)
query = {"sandbox_id": "398"}  # Replace with your desired criteria
filtered_documents = collection.find(query)

# # Loop through filtered documents and print them
i = 0
for document in filtered_documents:
    i += 1
    # print("--", document)
print(f"sandbox_id = 398 entries: {i}")
