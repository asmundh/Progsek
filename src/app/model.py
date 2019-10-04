import mysql.connector

# Access database using mysql connector package
db = mysql.connector.connect(
    user='root', 
    password='root',
    host='10.5.0.5',
    database='db'
)

def get_users():
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

def match_user(username, password):
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = (%s) and password = (%s)")
    cursor.execute(query, (username, password))
    user = cursor.fetchall()
    return user

def register_user(username, password):
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, (%s), (%s))")
    cursor.execute(query, (username, password))
    cursor.close()
