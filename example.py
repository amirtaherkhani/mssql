import pymssql # more info https://pymssql.readthedocs.io/en/stable/pymssql_examples.html
import pandas as pd 
import names
import os 
import random
from dotenv import load_dotenv
load_dotenv()

SERVER = 'localhost' # to specify an alternate port
USERNAME = 'sa' 
PASSWORD = os.environ.get('MSSQL_SA_PASSWORD')
DATABASE = 'master' 
TABLE_NAME="persons"

def generate_data(count:int)->pd.DataFrame:
	list_name=[]
	for x in range(0, count):
		list_name.append((names.get_full_name(gender='male'),"male",(random.randint(1, 80))))	
		list_name.append((names.get_full_name(gender='female'),"female",(random.randint(1, 80))))
	return pd.DataFrame.from_records(list_name, columns =['name', 'gender','age'])

conn = pymssql.connect(SERVER,USERNAME, PASSWORD,DATABASE,autocommit=True)
cursor = conn.cursor()

df=generate_data(100)

## read data as df 
cursor.execute("""
if not exists (select * from sysobjects where name='{}' and xtype='U')
{}""".format(TABLE_NAME,pd.io.sql.get_schema(df.reset_index(), TABLE_NAME)))

## write data as df 

##data most be list of tupe ->> [(),(),...()]
sql="""
		INSERT INTO {} ({})
		VALUES (%s, %s, %d)""".format(TABLE_NAME," ,".join(df.columns.to_list()))
                                
cursor.executemany(sql, list(df.itertuples(index=False)))

conn.close()

with pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE) as conn:
    with conn.cursor(as_dict=True) as cursor:           
        cursor.execute("SELECT * from persons")
        data=cursor.fetchall()
df=pd.DataFrame(data)
print(df)   

