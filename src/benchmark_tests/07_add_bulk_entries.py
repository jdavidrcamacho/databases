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

total_vals_mongo, total_vals_std_mongo = [], []
total_vals_postgre, total_vals_std_postgre = [], []
times_mongo, times_postgre = [], []

# Define the number of entries to generate (adjust as needed)
num_entries = 10000
i = 100
for ii in range(i):
    print(f"PostgreSQL - Run {ii}")
    data = []
    for _ in range(num_entries):
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
    connection_string = (f"dbname={database} user={user} password={password} "
                         f"host={host} port={port}")
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user, password=password)
    cur = conn.cursor()
    # Construct the insert query with placeholders
    query = """
    INSERT INTO table_example (timestamp_str, sandbox_id, pool_id, cmd,
                               username, wd, hostname, ip, cmd_type, tags)
    VALUES (%(timestamp_str)s, %(sandbox_id)s, %(pool_id)s, %(cmd)s,
            %(username)s, %(wd)s, %(hostname)s, %(ip)s, %(cmd_type)s,
            %(tags)s);
    """
    # Execute bulk insert (replace with your generated data)
    cur.executemany(query, data)

    # Commit changes and end time measurement
    conn.commit()
    # Close the connection
    conn.close()
    times_postgre.append(time()-start)
total_vals_postgre.append(np.mean(times_postgre))
total_vals_std_postgre.append(np.std(times_postgre))


for ii in range(i):
    print(f"mongoDB - Run {ii}")
    data = []
    for _ in range(num_entries):
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
    # Connect to MongoDB (with error handling)
    client = MongoClient("localhost", 27017)  # type: ignore
    db = client["my_database"]
    collection = db["my_collection"]

    # Insert data using insert_many
    result = collection.insert_many(data, ordered=False)
    times_mongo.append(time()-start)
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))


plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Add 10k new entries')

plt.bar(['postgreSQL', 'mongoDB'],
        [total_vals_postgre[0], total_vals_mongo[0]])
plt.errorbar(['postgreSQL', 'mongoDB'],
             [total_vals_postgre[0], total_vals_mongo[0]],
             yerr=[total_vals_std_postgre[0], total_vals_std_mongo[0]],
             fmt="o", color="r")
plt.ylabel('Time (s)')
plt.xlabel('Database')
plt.show()
