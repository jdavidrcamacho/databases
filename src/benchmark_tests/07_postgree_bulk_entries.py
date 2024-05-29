import psycopg2  # type: ignore
from time import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from bson import ObjectId

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


# Define the number of entries to generate (adjust as needed)
num_entries = 1000
# Sample data structure (replace with your actual column names)
data = []
for ii in range(num_entries):
    data.append({
        "_id": f"{ObjectId()}",
        "timestamp_str": "2024-05-24T10:00:00",
        "sandbox_id": f"{ii+10}",
        "pool_id": f"{ii+10}",
        "cmd": "echo hello world",
        "username": "new_user",
        "wd": "/home/test",
        "hostname": f"host-{ii+10}",
        "ip": f"10.0.{ii+10}.{ii+10}",
        "cmd_type": "example_entry",
        "tags": ["test", "example"],
    })

# Docker container details
host = "localhost"
port = 5433
database = "postgres_database"
user = "root"
password = "pass123"

# Connecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)
cursor = conn.cursor()

postgreSQL_select_Query = "SELECT * FROM table_example"
cursor.execute(postgreSQL_select_Query)
records = cursor.fetchall()
print(f"Initial DB entries: {len(records)}")


total_vals_postgre, total_vals_std_postgre = [], []
times_postgre = []

i = 5000
for ii in range(i):
    print(f"Run {ii}")
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

# Reconnecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)
cursor = conn.cursor()

postgreSQL_select_Query = "SELECT * FROM table_example"
cursor.execute(postgreSQL_select_Query)
records = cursor.fetchall()
print(f"Final DB entries: {len(records)}")

# Initial DB entries: 19848
# Final DB entries: 2019848
plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.title('PostgreSQL bulk data insertion')
plt.plot(times_postgre, 'o')
plt.ylabel('Time (s)')
plt.xlabel('Iteration')
plt.show()


