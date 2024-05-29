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

i = 100

total_vals_mongo, total_vals_std_mongo = [], []
total_vals_postgre, total_vals_std_postgre = [], []
times_mongo, times_postgre = [], []

for ii in range(i):
    start = time()
    connection_string = (f"dbname={database} user={user} password={password} "
                         f"host={host} port={port}")
    print(f"\nConnecting using: {connection_string}\n")
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user, password=password)
    cur = conn.cursor()

    # Define new entry data (replace with your actual values)
    new_entry = {
        "timestamp_str": "2024-05-24T10:00:00",
        "sandbox_id": f"{1000+ii}",
        "pool_id": "11",
        "cmd": "echo hello world",
        "username": "new_user",
        "wd": "/home/test",
        "hostname": "my-server",
        "ip": "192.168.1.10",
        "cmd_type": "example_entry",
        "tags": ["test", "example"],
    }

    # Construct the insert query with placeholders
    query = """
    INSERT INTO table_example (timestamp_str, sandbox_id, pool_id, cmd,
                               username, wd, hostname, ip, cmd_type, tags)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    # Prepare the query with data (prevents SQL injection)
    cur.execute(query, tuple(new_entry.values()))
    # Commit the changes to the database
    conn.commit()
    print("New entry added successfully!")
    # Close the connection
    conn.close()
    times_postgre.append(time()-start)
total_vals_postgre.append(np.mean(times_postgre))
total_vals_std_postgre.append(np.std(times_postgre))

for ii in range(i):
    start = time()
    # Connect to MongoDB (with error handling)
    try:
        client = MongoClient("localhost", 27017)  # type: ignore
    except pymongo.errors.ConnectionFailure:
        print("Error: Could not connect to MongoDB server.")
        exit(1)
    db = client["my_database"]
    collection = db["my_collection"]

    # Define new entry data (replace with your actual values)
    new_entry = {
        "hostname": "attacker",
        "ip": "10.1.26.23",
        "timestamp_str": "2024-05-24T10:00:00",  
        "sandbox_id": f"{1000+ii}",
        "cmd": "echo hello world",
        "pool_id": "11",
        "wd": "/home/test",
        "cmd_type": "example_entry",
        "username": "new_user",
        "tags": ["test", "example"],
    }
    # Insert the new entry
    result = collection.insert_one(new_entry)
    # Print the inserted document ID
    print(f"New entry inserted with ID: {result.inserted_id}")
    times_mongo.append(time()-start)
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Add a new entry')

plt.bar(['postgreSQL', 'mongoDB'],
        [total_vals_postgre[0], total_vals_mongo[0]])
plt.errorbar(['postgreSQL', 'mongoDB'],
             [total_vals_postgre[0], total_vals_mongo[0]],
             yerr=[total_vals_std_postgre[0], total_vals_std_mongo[0]],
             fmt="o", color="r")
plt.ylabel('Time (s)')
plt.xlabel('Database')
# plt.savefig('sunspotsNumber.png', bbox_inches='tight')
plt.show()
# plt.close('all')