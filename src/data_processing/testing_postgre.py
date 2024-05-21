import psycopg2  # type: ignore

# Docker container details
host = "localhost"
port = 5432
database = "database_example"
user = "postgres"
password = "pass123"
connection_string = f"dbname={database} user={user} password={password} host={host} port={port}"
print(f"Connecting using: {connection_string}")

conn = psycopg2.connect(host=host, port=port, database=database,
                        user=user, password=password)


# try:
#     # Connect to the database
#     conn = psycopg2.connect(
#         host=host, port=port, database=database, user=user, password=password
#     )

#     # Create a cursor object
#     cur = conn.cursor()

#     # Execute a query (replace with your desired query)
#     cur.execute("SELECT * FROM your_table")

#     # Fetch results
#     rows = cur.fetchall()

#     # Process results (e.g., print data)
#     for row in rows:
#         print(row)

#     # Commit changes (if necessary)
#     # conn.commit()

# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to PostgreSQL", error)

# finally:
#     # Close the cursor and connection
#     if cur is not None:
#         cur.close()
#     if conn is not None:
#         conn.close()

# print("Connection to PostgreSQL Docker container closed.")
