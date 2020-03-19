#!/usr/bin/python

import hmac, base64, struct, hashlib, time, json, os
import string, random
from PIL import Image
import qrcode
import shutil


def get_hotp_token(secret, intervals_no):
    """This is where the magic happens."""
    key = base64.b32decode(normalize(secret), True)  # True is to fold lower into uppercase
    msg = struct.pack(">Q", intervals_no)
    h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
    o = h[19] & 15
    h = str((struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000)
    return prefix0(h)


def get_totp_token(secret):
    """The TOTP token is just a HOTP token seeded with every 30 seconds."""
    return get_hotp_token(secret, intervals_no=int(time.time()) // 30)


def normalize(key):
    """Normalizes secret by removing spaces and padding with = to a multiple of 8"""
    k2 = key.strip().replace(' ', '')
    # k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
    if len(k2) % 8 != 0:
        k2 += '=' * (8 - len(k2) % 8)
    return k2


def prefix0(h):
    """Prefixes code with leading zeros if missing."""
    if len(h) < 6:
        h = '0' * (6 - len(h)) + h
    return h


def generate_key_dict():
    """
    Generates the key dictionary with TOTP keys based on secrets.json
    :return: dictionary of keys
    """
    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'secrets.json'), 'r') as f:
        secrets = json.load(f)

    key_dict = {}
    for label, key in sorted(list(secrets.items())):
        key_dict[label] = get_totp_token(key)
        print("{}:\t{}".format(label, get_totp_token(key)))
    return key_dict


### Code for verifying key and creating QR


def generate_url(label, user, key, digits=6, period=30):
    """
    Generate url for google auth qr
    https://dan.hersam.com/tools/gen-qr-code.html
    :param label: website
    :param user: email
    :param key: key from secrets.json
    :param digits: something
    :param period: how long code will be active
    :return: url
    """
    url = "otpauth://totp/" + label + \
          ":" + user + \
          "?secret=" + key + \
          "&issuer=" + label + \
          "&digits=" + str(digits) + \
          "&period=" + str(period)

    return url


# TODO: currently not in use, consider delete
def generate_qrcode(url):
    """
    Genererates qr and overwrites old one
    :param url: google auth url
    :return:
    """
    try:
        img = qrcode.make(url)
        img.save("qrcode.png")
        img_path = shutil.copy('qrcode.png', '../static/qrcode.png')
    except IOError as e:
        print(e)


def validate_key(username, proposed_key):
    """
    Matches username to key and validates if it is correct
    :param username: username
    :param proposed_key: key from input form
    :return: true if correct, false otherwise
    """
    actual_key = get_temp_key(username)
    if actual_key == str(proposed_key):
        return True
    return False


def add_to_secrets(username):
    """
    Adds username:key row to secrets.json with random uppercase "secret" key and username
    :param username:
    :return:
    """
    key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
    keypair = {username: key}
    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'secrets.json'), 'r') as f:
        secrets = json.load(f)

    secrets.update(keypair)
    with open(os.path.join(rel, 'secrets.json'), 'w') as f:
        json.dump(secrets, f)


def get_key(username):
    """
    Returns
    :param username:
    :return:
    """
    rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(rel, 'secrets.json'), 'r') as f:
        keys = json.load(f)
    return keys[username]


def get_temp_key(username):
    """
    Returns current TOTP key based on username
    :param username:
    :return: TOTP key
    """
    keys = generate_key_dict()
    return keys[username]
