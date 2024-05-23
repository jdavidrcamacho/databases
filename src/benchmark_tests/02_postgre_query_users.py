import psycopg2  # type: ignore
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


# Docker container details
host = "localhost"
port = 5433
database = "root"
user = "root"
password = "pass123"
table_name = "table_example"

connection_string = (f"dbname={database} user={user} password={password} "
                     f"host={host} port={port}")
print(f"\nConnecting using: {connection_string}\n")
conn = psycopg2.connect(host=host, port=port, database=database,
                        user=user, password=password)

cur = conn.cursor()

# Define the list of usernames
usernames = ["root", "admin", "vagrant", "None", "student", "user-access",
             "kali", "eve", "user", "bob", "cni"]
total_count = [7261, 2166, 15, 4836, 86, 859,
               4171, 293, 78, 71, 12]

counts, times = [], []
for _ in range(1):
    # Loop through each username
    for username in usernames:
        start = time()
        # Construct the query with dynamic username
        query = """
            SELECT COUNT(*)
            FROM table_example
            WHERE username = %s;
        """

        # Execute the query with username parameter
        cur.execute(query, (username,))

        # Fetch the count result (should be a single value)
        count = cur.fetchone()[0]

        # Print the username and count
        print(f"Username: {username}, Count: {count}")
        counts.append(count)
        times.append(time()-start)
# Close the connection
conn.close()

print(counts)
print(times)

plt.rcParams['figure.figsize'] = [15, 10]
plt.figure()
plt.plot(times, counts, '.', color='blue', markersize=20, label='postgreSQL')
plt.xlabel('Time (s)')
plt.ylabel('Number of entries')
plt.tight_layout(h_pad=0.7, w_pad=0.7)
plt.legend()
# plt.savefig('sunspotsNumber.png', bbox_inches='tight')
plt.show()
# plt.close('all')
