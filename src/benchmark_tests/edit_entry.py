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


i = 100
total_vals_mongo, total_vals_std_mongo = [], []
total_vals_postgre, total_vals_std_postgre = [], []
times_mongo, times_postgre = [], []
for ii in range(i):
    start = time()
    connection_string = (f"dbname={database} user={user} password={password} "
                         f"host={host} port={port}")
    conn = psycopg2.connect(host=host, port=port, database=database,
                            user=user, password=password)
    cur = conn.cursor()

    update_data = {
        "pool_id": ii,  # New pool_id value
    }
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

    cur.execute(query, {**update_data, **criteria})
    conn.commit()
    print("Entry updated successfully!")
    conn.close()
    times_postgre.append(time()-start)
total_vals_postgre.append(np.mean(times_postgre))
total_vals_std_postgre.append(np.std(times_postgre))

for ii in range(i):
    start = time()
    client = MongoClient("localhost", 27017)  # type: ignore
    db = client["my_database"]
    collection = db["my_collection"]

    criteria = {
        "hostname": "attacker",
        "ip": "10.1.26.23",
        "timestamp_str": "2021-05-25T08:54:59.258Z",
        "sandbox_id": "33",
        "cmd": "fcrackzip --dictionary ../.invoices2019.zip",
        "username": "user-access",
    }

    update_data = {
        "$set": {"pool_id": ii}  # type: ignore
        }
    result = collection.find_one_and_update(criteria, update_data)

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
plt.show()
