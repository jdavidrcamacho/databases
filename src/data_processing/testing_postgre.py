import psycopg2  # type: ignore
import pandas as pd  # type: ignore
from sqlalchemy import create_engine

# Docker container details
host = "localhost"
port = 5433
database = "root"
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
# table_creation = '''
#    CREATE TABLE table_example (
#        cmd_type TEXT NOT NULL,
#        pool_id TEXT NOT NULL,
#        sandbox_id TEXT NOT NULL,
#        timestamp_str TEXT NOT NULL,
#        hostname TEXT NOT NULL,
#        cmd TEXT NOT NULL,
#        ip TEXT NOT NULL,
#        username TEXT NOT NULL,
#        wd TEXT NOT NULL
#    )
# '''
# cur.execute(table_creation)

# Create an SQLAlchemy engine
engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{database}",
)

df = df.astype(str)
df.drop_duplicates(subset=None)
df.to_sql(table_name, engine, method='multi', if_exists="replace", index=False)

conn.commit()
cur.close()
conn.close()

# Reconnecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)


cursor = conn.cursor()
# drop table accounts
postgreSQL_select_Query = "SELECT * FROM table_example"
# Executing the query
cursor.execute(postgreSQL_select_Query)

print("\nSELECT * FROM table_example:")
records = cursor.fetchall()
print(records)


# Reconnecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)


cursor = conn.cursor()
# drop table accounts
sql = '''DROP TABLE table_example '''
# Executing the query
cursor.execute(sql)
print("\nTable dropped!")

# Commit changes  and close connection to the database
conn.commit()
conn.close()
