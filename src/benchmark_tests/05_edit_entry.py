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

    # Define the data to update (replace with actual values)
    update_data = {
        "pool_id": ii,  # New pool_id value
    }

    # Criteria to identify the entry (replace with actual values)
    criteria = {
        "hostname": "attacker",
        "ip": "10.1.26.23",
        "timestamp_str": "2021-05-25T08:54:59.258Z",
        "sandbox_id": "33",
        "cmd": "fcrackzip --dictionary ../.invoices2019.zip",
        "username": "user-access",
    }

    # Construct the UPDATE query with placeholders
    query = """
    UPDATE table_example
    SET pool_id = %(pool_id)s
    WHERE hostname = %(hostname)s
    AND ip = %(ip)s
    AND timestamp_str = %(timestamp_str)s
    AND sandbox_id = %(sandbox_id)s
    AND cmd = %(cmd)s
    AND username = %(username)s;
    """

    # Prepare the query with data (prevents SQL injection)
    cur.execute(query, {**update_data, **criteria})
    # Commit the changes to the database
    conn.commit()
    print("Entry updated successfully!")
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

    # Define the criteria to identify the entry (replace with actual values)
    criteria = {
        "hostname": "attacker",
        "ip": "10.1.26.23",
        "timestamp_str": "2021-05-25T08:54:59.258Z",
        "sandbox_id": "33",
        "cmd": "fcrackzip --dictionary ../.invoices2019.zip",
        "username": "user-access",
    }

    # Update data (replace with new pool_id value)
    update_data = {
        "$set": {"pool_id": ii}  # type: ignore
        }

    # Update the entry using find_one_and_update
    result = collection.find_one_and_update(criteria, update_data)

    # Check if update was successful (result will be None if not found)
    if result:
        print(f"Entry updated successfully. Updated document:\n{result}")
    else:
        print("Entry not found for update.")
    times_mongo.append(time()-start)
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))


plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Update existing entry')

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
