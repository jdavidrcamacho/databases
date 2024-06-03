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
    entry_user = f"{1000+ii}"
    query = """
    DELETE FROM table_example
    WHERE sandbox_id = %s;
    """
    cur.execute(query, (entry_user,))
    conn.commit()
    print(f"Entry with ID {entry_user} deleted successfully!")
    conn.close()
    times_postgre.append(time()-start)
total_vals_postgre.append(np.mean(times_postgre))
total_vals_std_postgre.append(np.std(times_postgre))


for ii in range(i):
    start = time()
    client = MongoClient("localhost", 27017)  # type: ignore
    db = client["my_database"]
    collection = db["my_collection"]

    entry_user = f"{1000+ii}"
    result = collection.delete_one({"sandbox_id": entry_user})
    if result.deleted_count == 1:
        print(f"Entry with username {entry_user} deleted successfully!")
    else:
        print("Entry not found for deletion.")
    times_mongo.append(time()-start)
total_vals_mongo.append(np.mean(times_mongo))
total_vals_std_mongo.append(np.std(times_mongo))

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('Delete a entry')
plt.bar(['postgreSQL', 'mongoDB'],
        [total_vals_postgre[0], total_vals_mongo[0]])
plt.errorbar(['postgreSQL', 'mongoDB'],
             [total_vals_postgre[0], total_vals_mongo[0]],
             yerr=[total_vals_std_postgre[0], total_vals_std_mongo[0]],
             fmt="o", color="r")
plt.ylabel('Time (s)')
plt.xlabel('Database')
plt.show()
