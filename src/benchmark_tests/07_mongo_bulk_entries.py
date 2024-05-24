from pymongo import MongoClient
from time import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# from bson import ObjectId

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False})
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.linewidth'] = 2
plt.close('all')

font = {'size': 25}
matplotlib.rc('font', **font)

total_vals_mongo, total_vals_std_mongo = [], []
times_mongo = []

# Connect to MongoDB (with error handling)
client = MongoClient("localhost", 27017)  # type: ignore
db = client["my_database"]
collection = db["my_collection"]

cursor = collection.find({}, {"_id": 1})
ids = []
for document in cursor:
    ids.append(document["_id"])

# Define the number of entries to generate (adjust as needed)
num_entries = 1000
i = 5000
for ii in range(i):
    print(f"Run {ii}")
    data = []
    for ii in range(num_entries):
        data.append({
            "timestamp_str": "2024-05-24T10:00:00",
            "sandbox_id": f"{np.random.randint(0,100000)}+",
            "pool_id": f"{np.random.randint(0,100000)}",
            "cmd": "echo hello world",
            "username": "new_user",
            "wd": "/home/test",
            "hostname": f"host-{np.random.randint(0,100000)}",
            "ip": f"10.0.{np.random.randint(0,10)}.{np.random.randint(0,10)}",
            "cmd_type": "example_entry",
            "tags": ["test", "example"],
        })
    start = time()

    client = MongoClient("localhost", 27017)  # type: ignore
    db = client["my_database"]
    collection = db["my_collection"]
    # Insert data using insert_many
    # collection.drop_indexes()
    result = collection.insert_many(data)
    # client.close()
    times_mongo.append(time()-start)
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))

# Find all documents in the collection
all_documents = collection.find()
num_entries = len(list(all_documents.clone()))
print(f"DB entries: {num_entries}")


# plt.rcParams['figure.figsize'] = [15, 10]
# plt.figure()
# plt.title('Mongo bulk data insertion')
# plt.plot(times_mongo, 'o')
# plt.ylabel('Time (s)')
# plt.xlabel('Iteration')
# plt.show()
