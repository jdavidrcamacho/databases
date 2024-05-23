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
df = pd.read_parquet("src/data/FullData.parquet")
df = df.astype(str)

# Create a cursor object
cur = conn.cursor()
table_name = "table_example"

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
records = cursor.fetchall()
print(f"DB entries: {len(records)}")
