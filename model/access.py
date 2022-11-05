"""
Access to the application is controlled from here.
Passwords in the DB are MD5 encoded

The only valid user/pass combos are
    "bob" / "b"
    "nick" / "z"
    "todd" / "x"
"""

import hashlib
#import model.network.jsn_drop_service as json
import requests
import json

def is_password_valid(login, password):
    """
    Checks that the given login and password pair is valid.

    Args:
        string: A login name
        string: The (plaintext) password to check
    Returns:
        True/False: Is the given password the right one for the given login name
    """
    md5pass = hashlib.md5(password.encode('utf-8')).hexdigest()

    if login == "bob" and md5pass == "92eb5ffee6ae2fec3ad71c777531578f":
        return True
    elif login == "nick" and md5pass == "fbade9e36a3f36d3d676c1b808451dd7":
        return True
    elif login == "todd" and md5pass == "9dd4e461268c8034f5c8564e155c67a6":
        return True
    else:
        return False
