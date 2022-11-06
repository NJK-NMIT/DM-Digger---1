"""
Access to the application is controlled from here.
Passwords in the DB are MD5 encoded (not salted)

Hint: The default valid user/pass combos are:
    "bob" / "b"
    "nick" / "z"
    "todd" / "x"
"""

import hashlib
import sys
import re
import model.network.jsn_drop_service as json



def stderr_print(*args, **kwargs):
    """Because sometimes you want to print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


def is_password_valid(login, password):
    """
    Checks that the given login and password pair is valid.
    Authentification interface errors are reported on STDERR

    Args:
        string: A login name
        string: The (plaintext) password to check
    Returns:
        True/False: Is the given password the right one for the given login name
    """

    # No login, no auth
    if not login:
        return False

    # Minimal effort to stop people trying to play silly buggers
    if "'" in login:
        return False

    # Passwords are stored in MD5 format
    md5pass = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Get the hashed password for the requested user
    # TODO: Have some error handling around timeout, service down, domain expired, etc
    jsnDrop = json.jsnDrop()
    result = jsnDrop.select("dm_users",f"User_ID = '{login}'")
 
    # User doesn't exist?  That's a fail
    if ("DATA_ERROR" in jsnDrop.jsnStatus):
        return False
 
    # No service authentication?  That's a (reported) fail
    if ("AUTH_ERROR" in jsnDrop.jsnStatus):
        stderr_print("JSON Authentication error.  Make sure your auth key hasn't expired.")
        return False

    # We have a (single) response so extract the password field
    auth_pass = result[0]["password"]

    # Bad MD5 password?  That's a (reported) fail
    # But if someone can hack the auth table, they can update the password
    #   to something they know anyway.  So what really is the point?
    if len(auth_pass) != 32:
        stderr_print(f"Auth password for {login} is not the correct length.")
        return False
    # Is this just an excuse to use regular expressions?
    if not re.match('^[0-9a-z]{32}$', auth_pass):
        stderr_print(f"Auth password for {login} is not in the correct format.")
        return False
        
    # Does the given password match that of the user?
    if auth_pass == md5pass:
        return True
    else:
        return False
    
