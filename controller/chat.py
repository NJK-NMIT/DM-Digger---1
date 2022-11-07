"""
Chat stuff

"""

import model.network.jsn_drop_service as json
import view.View_dm



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
    max_message_len = 60
    message = values["-CHATSEND-"]
    if len(message) > max_message_len:
        return(f"'{message} is too long. {max_message_len} max.")
    if not message:
        return("No message to send")

    user = dm.get_login()
    timestamp = dm.now()

    # Store the message
    jsnDrop = json.jsnDrop()
    result = jsnDrop.store("dm_chat",[{"User_ID":user, "Message":message, "Timestamp":timestamp}])
    if "Data error" in result:
        return(result)

    # Record this most recent chat timestamp.
    dm.set_chat_timestamp(timestamp)

    # Reshow chats immediately to include our new one
    view.View_dm.show_chat(win, dm)

    return(f"Sent: {message}")


def fetch():
    """Get all the chat messages"""
    jsnDrop = json.jsnDrop()
    result = jsnDrop.select("dm_chat","1 = 1")
    sorted_result = sorted(result, key=lambda x: x['Timestamp']) 
    return(sorted_result)


# Why the bloody hell is this so slow?
def remove_chats(keys) -> None:
    """Delete the chats that match the given keys (Timestamps)"""
    jsnDrop = json.jsnDrop()

    for key in keys:
        result = jsnDrop.delete("dm_chat", f"Timestamp='{key}'")


def remove_old_chats(key) -> None:
    """Remove the chats older than the given key."""
    jsnDrop = json.jsnDrop()
    result = jsnDrop.delete("dm_chat", f"Timestamp<'{key}'")
