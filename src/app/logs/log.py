from datetime import datetime, timedelta
import os, json, random, string
from json.decoder import JSONDecodeError

def format_string(operation, ip, parameters):
    """
    Formats a string to be written to file
    :param operation: what is trying to be done
    :param ip: ip of user
    :param parameters: list of tuples, [(variable, value),(..),...]
    :return: one line string
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    line = ("%s | %s | %s;" % (timestamp, ip, operation.upper()))

    for val in parameters:
        line += (" %s : %s," % (val[0], val[1]))

    line = line[:-1]
    line += "\n"

    return line


def write_requests(operation, ip, parameters):
    """
    Writes log to "requests.txt" file

    :param operation: what is trying to be done
    :param ip: ip of user
    :param parameters: list of tuples of strings, [(variable, value),(..),...]
    :return: one line string
    """
    line = format_string(operation, str(ip), parameters)

    with open("logs/requests.txt", "a") as file:
        file.write(line)


def print_file(filename):
    """
    Prints file
    :param filename: name of file within folder
    :return:
    """

    with open(filename, "r") as file:
        print(file.read())


def write_to_logins(ip):
    """
    JSON format:
    {
        "ip": {
            "last_attempt":str(datetime),
            "number_of_attempts":int
        }
    }
    :param ip: str with ip
    :return: false if more than 4 attempts in 5 mins, true otherwise
    """
    last_attempt_string = 'last_attempt'
    number_of_attempts_string = 'number_of_attempts'

    ok = True

    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'logins.json'), 'r') as f:
        logins = json.load(f)

    if ip in logins:
        last_attempt = logins[ip][last_attempt_string]
        delta = get_time_difference(datetime.strptime(last_attempt, "%m/%d/%Y, %H:%M:%S"))
        print("DELTA: {}".format(delta))
        number_of_attempts = logins[ip][number_of_attempts_string]

        if delta < 5 and number_of_attempts > 4:
            ok = False
        elif delta >= 5:
            logins[ip][number_of_attempts_string] = 1
        else:
            logins[ip][number_of_attempts_string] += 1

        logins[ip][last_attempt_string] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    else:
        logins[ip] = {
            "last_attempt": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "number_of_attempts": 1
        }

    with open(os.path.join(rel, 'logins.json'), 'w') as f:
        json.dump(logins, f, indent=2)
        #print_logins()

    return ok


def remove_from_logins(ip):
    """
    Remove user from logins, not in use
    :param ip: ip of user
    :return:
    """
    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'logins.json'), 'r') as f:
        logins = json.load(f)

    try:
        del logins[ip]
    except KeyError:
        print("Key %s not found" % ip)
        pass

    with open(os.path.join(rel, 'logins.json'), 'w') as f:
        json.dump(logins, f, indent=2)


def get_time_difference(lastAttemptTime, timeNow=datetime.now()):
    """
    Gets difference in minutes between two datetimes
    :param pre: datetime object
    :param post:  datetime object, now if not passed
    :return: difference in minutes
    """
    timediff = (timeNow - lastAttemptTime) / timedelta(minutes=1)
    return  timediff 
    # return (lastAttemptTime - timeNow) / timedelta(minutes=1)


def print_logins():
    """

    :return:
    """
    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'logins.json'), 'r') as f:
        logins = json.load(f)

    json_formatted_str = json.dumps(logins, indent=2)

    print(json_formatted_str)
