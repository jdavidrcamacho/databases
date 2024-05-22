import pymongo

# Replace with your connection details
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db["your_collection_name"]


# Insert operation
def insert_data(data):
    result = collection.insert_one(data)
    return result.inserted_id


# Read operation (assuming a unique field 'id')
def read_data(id):
    document = collection.find_one({"id": id})
    return document


# Update operation (assuming a unique field 'id')
def update_data(id, update_data):
    result = collection.update_one({"id": id}, {"$set": update_data})
    return result.matched_count


# Delete operation (assuming a unique field 'id')
def delete_data(id):
    result = collection.delete_one({"id": id})
    return result.deleted_count

# Benchmarking logic here (e.g., measure time for multiple inserts/reads)
