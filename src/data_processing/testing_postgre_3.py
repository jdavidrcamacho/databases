import psycopg2  # type: ignore

# Docker container details
host = "localhost"
port = 5433
database = "root"
user = "root"
password = "pass123"

conn = psycopg2.connect(host=host, database=database, user=user,
                        password=password, port=port)

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
