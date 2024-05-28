import pymysql

hostname = 'database-1.cde4044wig4c.ap-south-1.rds.amazonaws.com'
port = 3306 
dbname = 'Geocery_new'
username = 'Santhosh'
password = 'Iamingood'

con= pymysql.connect(
    host=hostname,
    port=port,
    user=username,
    password=password,
    database=dbname
)
customer=con.cursor()
vl=int(901)

customer.execute('''Select * from Admin Where Password=%s and Admin_ID=%s''',("Admin1@tcs",901))
data=customer.fetchall()
print(data)




