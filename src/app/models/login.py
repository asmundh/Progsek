from models.database import db

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

def get_user_id_by_name(username):
    cursor = db.cursor()
    query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    cursor.execute(query)
    try:
        userid = cursor.fetchall()[0][0]
    except:
        userid = None
    cursor.close()
    return userid

def get_user_name_by_id(userid):
    cursor = db.cursor()
    query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    cursor.execute(query)
    username = cursor.fetchall()[0][0]
    cursor.close()
    return username

def match_user(username, password):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    cursor.execute(query)
    user = cursor.fetchall()
    cursor.close()
    return user
