import psycopg2  # type: ignore
from pymongo import MongoClient
from time import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

# Docker container details
host = "localhost"
port = 5433
database = "postgres_database"
user = "root"
password = "pass123"

# Define the list of usernames
usernames = ["root", "admin", "vagrant", "None", "student", "user-access",
             "kali", "eve", "user", "bob", "cni"]
total_count = [7261, 2166, 15, 4836, 86, 859,
               4171, 293, 78, 71, 12]

i = 100
total_vals_mongo, total_vals_std_mongo = [], []
total_vals_postgre, total_vals_std_postgre = [], []
for u in usernames:
    connection_string = (f"dbname={database} user={user} password={password} "
                         f"host={host} port={port}")
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user, password=password)

    cur = conn.cursor()
    counts_postgre, times_postgre = [], []
    for _ in range(i):
        start = time()
        # Query to count entries for username 'bob'
        query = """
        SELECT COUNT(*)
        FROM table_example
        WHERE username = %s;
        """
        # Username to search for
        username = u

        # Execute query with username parameter
        cur.execute(query, (username,))

        # Fetch the count result (should be a single value)
        count = cur.fetchone()[0]
        counts_postgre.append(count)
        times_postgre.append(time()-start)
    # Close the connection
    conn.close()
    total_vals_postgre.append(np.mean(times_postgre))
    total_vals_std_postgre.append(np.std(times_postgre))

    # Connect to MongoDB 
    client = MongoClient("localhost", 27017)  # type: ignore
    db = client["my_database"]
    collection = db["my_collection"]

    # Use aggregation framework to group by username and count entries
    pipeline = [{"$group": {"_id": "$username", "count": {"$sum": 1}}}]

    counts_mongo, times_mongo = [], []
    for _ in range(i):
        start = time()
        # Username to search for
        username = u
        # Find documents with username 'bob' and count them
        count = collection.count_documents({"username": username})
        # Print the result
        counts_mongo.append(count)
        times_mongo.append(time()-start)
    total_vals_mongo.append(np.mean(times_mongo))
    total_vals_std_mongo.append(np.std(times_mongo))

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Search number of entries of a user')
plt.errorbar(total_count, total_vals_postgre, total_vals_std_postgre,
             marker='o', color='blue', markersize=8, ls='none',
             label='postgreSQL')
plt.errorbar(total_count, total_vals_mongo, total_vals_std_mongo,
             marker='o', color='red', markersize=8, ls='none', label='mongoDB')

plt.ylabel('Time (s)')
plt.xlabel('Number of entries')
plt.legend(loc='upper left')
plt.show()
