"""
Supervisor thread things go in here

"""

from time import sleep

import model.network.jsn_drop_service as json


# Reminder to self: Do not let the supervisor write to the window!
def supervisor(win, dm) -> None:
    """Keep polling for network events"""
    delay = 1.499 # 1499ms wait because primes are magic
    jsnDrop = json.jsnDrop()

    while dm.sup_keepalive():
        result = jsnDrop.select("dm_info","1 = 1")
        # Put the JSON into a dictionary
        val = {}
        for row in result:
            val[row["thing"]] = row["data"]
        print(f"{val['last_chat_ts']}  {dm.last_chat_ts}")
        # If the DB ts is newer than when we last displayed, we need to update the display
        if val['last_chat_ts'] > dm.last_chat_ts:
            dm.chat_needs_update = True
            print("Chat needs update")
            win.write_event_value('-SUP-', 'CHAT')

#        if val['last_data_ts'] > dm.last_data_ts:
#            dm.data_needs_update = True
#            print("Data needs update")

        sleep(delay)



def fetch():
    """Get all the chat messages"""
    jsnDrop = json.jsnDrop()
    result = jsnDrop.select("dm_chat","1 = 1")
    sorted_result = sorted(result, key=lambda x: x['Timestamp']) 
    return(sorted_result)


# Why is this so slow?
def remove_chats(keys) -> str:
    """Delete the chats that match the given keys (Timestamps)"""
    jsnDrop = json.jsnDrop()
    for key in keys:
        result = jsnDrop.delete("dm_chat", f"Timestamp='{key}'")
    return(result)


def remove_old_chats(key) -> str:
    """Remove the chats older than the given key."""
    jsnDrop = json.jsnDrop()
    result = jsnDrop.delete("dm_chat", f"Timestamp<'{key}'")
    return(result)
