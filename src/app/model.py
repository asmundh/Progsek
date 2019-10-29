import mysql.connector

def connect_to_db():
    try:
        # Access database using mysql connector package
        db = mysql.connector.connect(
            user='root', 
            password='root',
            host='10.5.0.5',
            database='db'
        )
    except Exception as e:
        print(e)
        print("Try connecting to local mysql database instead")
        # Access local database using mysql connector package
        db = mysql.connector.connect(
            user='root', 
            password='root',
            host='0.0.0.0',
            database='db'
        )
        pass
    return db

def get_users():
    db = connect_to_db()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users

def match_user(username, password):
    db = connect_to_db()
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    cursor.execute(query)
    user = cursor.fetchall()
    cursor.close()
    db.close()
    return user

def set_user(username, password):
    db = connect_to_db()
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, \"" + username + 
            "\", \"" + password + "\")")
    cursor.execute(query)
    cursor.close()
    db.close()

def get_guestbook_entries():
    db = connect_to_db()
    cursor = db.cursor()
    query = ("SELECT entryid, text FROM guestbook")
    cursor.execute(query)
    entries = cursor.fetchall()
    cursor.close()
    db.close()
    return entries

def set_guestbook_entry(entry):
    db = connect_to_db()
    cursor = db.cursor()
    query = ("INSERT INTO guestbook VALUES (NULL, \"" + entry + "\")")
    cursor.execute(query)
    cursor.close()
    db.close()    
