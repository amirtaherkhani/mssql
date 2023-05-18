import pymssql
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

SERVER = 'localhost' # to specify an alternate port
USERNAME = 'sa' 
PASSWORD = os.environ.get('MSSQL_SA_PASSWORD')
DATABASE = 'master' 

with pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE) as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute("""
        IF OBJECT_ID('persons', 'U') IS NOT NULL
            DROP TABLE persons
        CREATE TABLE persons (
            id INT NOT NULL,
            name VARCHAR(100),
            salesrep VARCHAR(100),
            PRIMARY KEY(id)
        )
        """)
        cursor.executemany(
            "INSERT INTO persons VALUES (%d, %s, %s)",
            [(1, 'John Smith', 'John Doe'),
            (2, 'Jane Doe', 'Joe Dog'),
            (3, 'Mike T.', 'Sarah H.')])
        # you must call commit() to persist your data if you don't set autocommit to True
        conn.commit()


with pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE) as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute("""
        CREATE PROCEDURE FindPerson
            @name VARCHAR(100)
        AS BEGIN
            SELECT * FROM persons WHERE name = @name
        END
        """)
        cursor.callproc('FindPerson', ('Jane Doe',))
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))
            
with pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE) as conn:
    with conn.cursor(as_dict=True) as cursor:           
        cursor.execute("SELECT * from persons")
        data=cursor.fetchall()
df=pd.DataFrame(data)
print(df)   