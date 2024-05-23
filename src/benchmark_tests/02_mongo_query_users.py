import pymongo
from pymongo import MongoClient
from time import time
import matplotlib
import matplotlib.pyplot as plt

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

# Connect to MongoDB (with error handling)
try:
    client = MongoClient("localhost", 27017)  # type: ignore
except pymongo.errors.ConnectionFailure:
    print("Error: Could not connect to MongoDB server.")
    exit(1)

db = client["my_database"]
collection = db["my_collection"]

# Use aggregation framework to group by username and count entries
pipeline = [
  {"$group": {"_id": "$username", "count": {"$sum": 1}}}
]

# Execute aggregation and fetch results
username_counts = collection.aggregate(pipeline)

counts, times = [], []
print("Username and Entry Count:")
for doc in username_counts:
    start = time()
    username = doc["_id"]
    count = doc["count"]
    counts.append(count)
    times.append(time()-start)
    print(f"Username: {username}, Count: {count}")

print(counts)
print(times)

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.plot(times, counts, '.', color='red', markersize=20, label='mongoDB')
plt.xlabel('Time (s)')
plt.ylabel('Number of entries')
plt.tight_layout(h_pad=0.7, w_pad=0.7)
plt.legend()
# plt.savefig('sunspotsNumber.png', bbox_inches='tight')
plt.show()
# plt.close('all')
