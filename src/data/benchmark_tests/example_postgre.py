import psycopg2

# Replace with your connection details
conn = psycopg2.connect(dbname="your_database_name", user="your_username", 
                        password="your_password", host="localhost")
cur = conn.cursor()


# Insert operation
def insert_data(data):
    # Replace with your insert query based on table schema
    cur.execute("INSERT INTO your_table (column1, column2, ...) VALUES (%s, %s, ...)", data)
    conn.commit()
    return cur.rowcount


# Read operation (assuming a unique field 'id')
def read_data(id):
    # Replace with your select query based on table schema
    cur.execute("SELECT * FROM your_table WHERE id = %s", (id,))
    return cur.fetchone()


# Update operation (assuming a unique field 'id')
def update_data(id, update_data):
    # Replace with your update query based on table schema
    cur.execute("UPDATE your_table SET column1 = %s, column2 = %s, ... WHERE id = %s", (*update_data, id))
    conn.commit()
    return cur.rowcount


# Delete operation (assuming a unique field 'id')
def delete_data(id):
    # Replace with your delete query based on table schema
    cur.execute("DELETE FROM your_table WHERE id = %s", (id,))
    conn.commit()
    return cur.rowcount

# Benchmarking logic here (e.g., measure time for multiple inserts/reads)

# Close connection after benchmarking
conn.close()
