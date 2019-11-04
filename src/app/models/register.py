from models.database import db

def set_user(username, password, full_name, company, phone_number, 
        street_address, city, state, postal_code, country):
    cursor = db.cursor()
    query = ("INSERT INTO users VALUES (NULL, \"" + username + "\", \"" + 
    password + "\", \"" + full_name + "\" , \"" + company + "\", \"" + 
    phone_number + "\", \"" + street_address + "\", \"" + city + "\", \"" +
    state  + "\", \"" + postal_code + "\", \"" + country + "\")")
    cursor.execute(query)
    cursor.close()
