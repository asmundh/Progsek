from models.database import db

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
    cursor.close()
    return user
