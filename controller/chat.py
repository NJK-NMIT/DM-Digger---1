"""
Chat stuff

"""


def send(win, dm, values):
    """
    Send a message to the chat system

    Args:
        string: Something
        string: Something
        obj: Window values
    Returns:
        True/False: Was the send successfull?
    """
    message = values["-CHATSEND-"]
    user = dm.get_login()

    if (message):
        return(f"Sent: {message}.\nBy {user}")
    else:
        return("No message to send")
