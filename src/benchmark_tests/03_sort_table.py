import psycopg2  # type: ignore
import pymongo
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

total_count = [1]

i = 10

total_vals_mongo, total_vals_std_mongo = [], []
total_vals_postgre, total_vals_std_postgre = [], []

counts_postgre, times_postgre = [], []
for _ in range(i):
    start = time()
    connection_string = (f"dbname={database} user={user} password={password} "
                         f"host={host} port={port}")
    print(f"\nConnecting using: {connection_string}\n")
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user, password=password)

    cur = conn.cursor()
    # Connect to your PostgreSQL database (replace details with yours)
    # Query to select all entries ordered by sandbox_id
    query = """
    SELECT *
    FROM table_example
    ORDER BY sandbox_id;
    """

    # Execute the query
    cur.execute(query)

    # Fetch the count result (should be a single value)
    count = cur.fetchall()

    # Print the username and count
    counts_postgre.append(count)
    times_postgre.append(time()-start)
    # Close the connection
    conn.close()
print(np.mean(times_postgre), np.std(times_postgre))
total_vals_postgre.append(np.mean(times_postgre))
total_vals_std_postgre.append(np.std(times_postgre))

counts_mongo, times_mongo = [], []
for _ in range(i):
    start = time()
    # Connect to MongoDB (with error handling)
    try:
        client = MongoClient("localhost", 27017)  # type: ignore
    except pymongo.errors.ConnectionFailure:
        print("Error: Could not connect to MongoDB server.")
        exit(1)
    db = client["my_database"]
    collection = db["my_collection"]
    # Find documents with username 'bob' and count them
    count = collection.find({}, sort={"$sort": {"sandbox_id": 1}})
    # Print the result
    counts_mongo.append(count)
    times_mongo.append(time()-start)
print(np.mean(times_mongo), np.std(times_mongo))
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Sorting a table by id')

plt.bar(['postgreSQL', 'mongoDB'], [total_vals_postgre[0],
                                    total_vals_mongo[0]])
plt.errorbar(['postgreSQL', 'mongoDB'],
             [total_vals_postgre[0], total_vals_mongo[0]],
             yerr=[total_vals_std_postgre[0], total_vals_std_mongo[0]],
             fmt="o", color="r")
plt.ylabel('Time (s)')
plt.xlabel('Database')
# plt.savefig('sunspotsNumber.png', bbox_inches='tight')
plt.show()
# plt.close('all')
