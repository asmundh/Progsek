from models.database import db
import mysql.connector

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        users = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    
    userid = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if(len(users)):
            userid = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    username = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if len(users):
            username = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
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
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    user = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if len(users):
            user = users[0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user

def verify_user_by_email(verification_key):
    is_real_key = match_verification_key(verification_key)

    db.connect()
    cursor = db.cursor()
    query = "UPDATE users SET verified = 1 WHERE verification_key = %s"

    try:
        cursor.execute(query, (verification_key,))
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        exit(1)
    finally:
        cursor.close()
        db.close()

def match_verification_key(verification_key):

    db.connect()
    cursor = db.cursor()
    query = "SELECT verification_key FROM users WHERE verification_key = %s AND verified = 0"
    result = ""
    try:
        cursor.execute(query, (verification_key,))
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
    finally:
        cursor.close()
        db.close()
    return result == verification_key

def check_if_user_is_verified_by_username(username):
    db.connect()
    cursor = db.cursor()
    query = "SELECT verified FROM users WHERE username = %s"
    result = ""

    try:
        cursor.execute(query, (username,))
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
    finally:
        cursor.close()
        db.close()
    return result == 1

def check_if_user_is_verified_by_verification_key(verification_key):
    db.connect()
    cursor = db.cursor()
    query = "SELECT verified FROM users WHERE verification_key = %s"
    result = ""
    try:
        cursor.execute(query, (verification_key,))
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
    finally:
        cursor.close()
        db.close()
    return result[0][0] == 1

