import pymssql # more info https://pymssql.readthedocs.io/en/stable/pymssql_examples.html
import pandas as pd 
import names


def generate_data()->list:
	list_name=[]
	for x in range(0, 5):
		list_name.append((names.get_full_name(gender='male'),"male"))	
		list_name.append((names.get_full_name(gender='female'),"female"))	
	return pd.DataFrame.from_records(list_name, columns =['name', 'gender'])



type_casting={"bigint":	"float64"	,
	"binary"	:"bytes"	,
	"bit"	:"bool"	,
	"char":	"str"	,
	"date":	"datetime"	,
	"datetime"	:"datetime"	,
	"float"	:"float64"	,
	"nchar"	:"str"	,
	"nvarchar":	"str"	,
	"nvarchar(max)":	"str"	,
	"real"	:"float64"	,
	"smalldatetime"	:"datetime"	,
	"smallint":	"int32"	,
	"tinyint"	:"int32"	,
	"uniqueidentifier":	"str"	,
	"varbinary":	"bytes"	,
	"varbinary(max)"	:"bytes"	,
	"varchar(n)"	:"str"	,
	"varchar(max)":	"str"}


	
host_name="localhost"
user_db="sa"
user_pass="AtgTsdWe3"
db_name="test"
table_name="persons"


conn = pymssql.connect(f"{host_name}", f"{user_db}", f"{user_pass}", f"{db_name}",autocommit=True)
cursor = conn.cursor()


## read data as df 
cursor.execute("""
if not exists (select * from sysobjects where name='persons' and xtype='U')
	create table persons (
		name VARCHAR(100),
		gender VARCHAR(100),
	)
""")




## write data as df 

df=generate_data()

# data most be list of tupe ->> [(),(),...()]
cursor.executemany("""
		INSERT INTO persons (name, gender)
		VALUES (%s, %s)""", list(df.itertuples(index=False)))


cursor.execute("""
SELECT * FROM {}
WHERE gender='male'
""".format(table_name))

result = cursor.fetchall()
df=pd.DataFrame.from_records(result, columns =['name', 'gender'])

print(df)

conn.close()

