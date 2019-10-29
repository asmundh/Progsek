from models.database import db

def set_user(username, password):
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, \"" + username + 
            "\", \"" + password + "\")")
    cursor.execute(query)
    cursor.close()
