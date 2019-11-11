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
