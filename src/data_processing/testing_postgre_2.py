import psycopg2  # type: ignore

# Docker container details
host = "localhost"
port = 5433
database = "root"
user = "root"
password = "pass123"

# Connecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)
# Create a cursor object
cursor = conn.cursor()
table_creation = '''
   CREATE TABLE staff_information (
       stf_id SERIAL PRIMARY KEY,
       stf_name TEXT NOT NULL
   )
'''
cursor.execute(table_creation)

conn.commit()
cursor.close()
conn.close()


# Reconnecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)

# Create a cursor object
cur = conn.cursor()
# Define a SELECT query to retrieve all data from the table
select_stmt = "SELECT * FROM staff_information"
# Execute the query
cur.execute(select_stmt)
# Fetch all rows from the result set
data = cur.fetchall()
# Check if any data was retrieved
if data:
    print("Data found in the table:")
    # Print each row of data
    for row in data:
        print(row)
else:
    print("No data found in the table.")

cursor.close()
conn.close()


# Reconnecting to database
conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)


cursor = conn.cursor()
# drop table accounts
sql = '''DROP TABLE staff_information '''
# Executing the query
cursor.execute(sql)
print("Table dropped!")

# Commit changes  and close connection to the database
conn.commit()
conn.close()
