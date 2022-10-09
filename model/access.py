"""
Access to the application is controlled from here

The only valid user/pass combos are
    "bob" / "x"
    "nick" / "x"
    "todd" / "x"
"""


def is_password_valid(login, password):
    """
    Checks that the given login and password pair is valid.

    Args:
        string: A login name
        string: The (plaintext) password to check
    Returns:
        True/False: Is the given password the right one for the given login name
    """
    if login == "bob" and password == "x":
        return True
    elif login == "nick" and password == "x":
        return True
    elif login == "todd" and password == "x":
        return True
    else:
        return False
