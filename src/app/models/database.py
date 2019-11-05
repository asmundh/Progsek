import mysql.connector

db = mysql.connector.connect(
    user='root', 
    password='root',
    #host='10.5.0.5',   # Docker address
    host='0.0.0.0',    # Local address
    database='db'
)
