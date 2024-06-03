import json
from pymongo import MongoClient
import psycopg2  # type: ignore
import pandas as pd  # type: ignore
from sqlalchemy import create_engine

# Docker container details
host = "localhost"
port = 5433
database = "postgres_database"
user = "root"
password = "pass123"

# Connect to MongoDB
client = MongoClient("localhost", 27017)  # type: ignore

db = client["my_database"]
collection = db["my_collection"]
collection.drop()  # Drop the collection (deletes all documents)

# Load JSON data
filenames = ["FullData.json"]
for filename in filenames:
    try:
        log_entries: list[dict[str, str]] = []
        with open(f"src/data/{filename}", "r") as f:
            for entry in f:
                try:
                    log_entries.append(json.loads(entry))
                except json.JSONDecodeError as e:
                    raise Exception(f"Error decoding JSON {filename}: {e}")
            collection.insert_many(log_entries)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
print("\nAll data loaded to mongoDB!")

# Find all documents in the collection
all_documents = collection.find()
num_entries = len(list(all_documents.clone()))
print(f"mongoDB entries: {num_entries}")

# Connect to postgreSQL
connection_string = (f"dbname={database} user={user} password={password} "
                     f"host={host} port={port}")
conn = psycopg2.connect(host=host, port=port, database=database,
                        user=user, password=password)

# Read the data using pandas
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
print("\nAll data loaded to postgreSQL!")
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
