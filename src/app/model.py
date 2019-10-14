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
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    cursor.execute(query)
    user = cursor.fetchall()
    return user

def set_user(username, password):
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, \"" + username + 
            "\", \"" + password + "\")")
    cursor.execute(query)
    cursor.close()

def get_guestbook_entries():
    cursor = db.cursor()
    query = ("SELECT entryid, text FROM guestbook")
    cursor.execute(query)
    entries = cursor.fetchall()
    cursor.close()
    return entries

def set_guestbook_entry(entry):
    cursor = db.cursor()
    query = ("INSERT INTO guestbook VALUES (NULL, \"" + entry + "\")")
    cursor.execute(query)
    cursor.close()
    
