import pymongo
import json
from pymongo import MongoClient

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
filenames = ["FullData.json"]
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
            collection.insert_many(log_entries)
        print(f"Data loaded successfully from {filename}!")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
print("\nAll data loaded!")

# Find all documents in the collection
all_documents = collection.find()
num_entries = len(list(all_documents.clone()))
print(f"DB entries: {num_entries}")
