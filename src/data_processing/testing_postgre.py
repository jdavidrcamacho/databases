import psycopg2  # type: ignore
import pandas as pd  # type: ignore
# import pyarrow.parquet as pq

# Docker container details
host = "localhost"
port = 5433
database = "database_example"
user = "root"
password = "pass123"

connection_string = (f"dbname={database} user={user} password={password} "
                     f"host={host} port={port}")
print(f"\nConnecting using: {connection_string}\n")

conn = psycopg2.connect(host=host, port=port, database=database,
                        user=user, password=password)

# Read the Parquet file using pandas
df = pd.read_parquet("src/data/sandbox.parquet")
df = df.astype(str)

# Create a cursor object
cur = conn.cursor()
table_name = "table_example"
table_creation = '''
   CREATE TABLE table_example (
       stf_id SERIAL PRIMARY KEY,
       cmd_type TEXT NOT NULL,
       pool_id TEXT NOT NULL,
       sandbox_id TEXT NOT NULL,
       timestamp_str TEXT NOT NULL,
       hostname TEXT NOT NULL,
       cmd TEXT NOT NULL,
       ip TEXT NOT NULL,
       username TEXT NOT NULL,
       wd TEXT NOT NULL
   )
'''
cur.execute(table_creation)

conn.commit()
cur.close()
conn.close()

# import sys
# sys.exit(0)

# # Define the insert statement with placeholders for data
# insert_stmt = f"""INSERT INTO {table_name} ({", ".join(df.columns)}) VALUES (%s, %s, ...)"""

# # Convert pandas DataFrame to a list of tuples (one tuple per row)
# data_tuples = df.to_records(index=False).tolist()

# # Execute the insert statement with data tuples
# cur.executemany(insert_stmt, data_tuples)

# # Commit the changes
# conn.commit()

# # Close the cursor and connection
# cur.close()
# conn.close()

# print(f"Parquet data uploaded to table {table_name}")
