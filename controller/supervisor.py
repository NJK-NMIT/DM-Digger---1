"""
Supervisor thread things go in here

"""

from time import sleep

import model.network.jsn_drop_service as json


# Reminder to self: Do not let the supervisor write to the window!
def supervisor(win, dm) -> None:
    """Keep polling for network events

    This thread will continously poll the dm_info table to see if the network
    information has changed.  When it does, this thread just flags that work
    needs to be done - it does not do it itself.
    """
    delay = 0.521 # 521ms wait between requests because primes are magic
    jsnDrop = json.jsnDrop()

    while dm.sup_keepalive():
        # Read all (both) values in one call
        result = jsnDrop.select("dm_info","1 = 1")
        val = {}
        for row in result:
            val[row["thing"]] = row["data"]
        # If the DB timestamp is newer than when we last displayed/imported,
        #   then we need to update the display/import
        # Don't indicate we need an update if we already know we need an update
        if (val['last_chat_ts'] > dm.last_chat_ts and not dm.chat_needs_update):
            print("Chat update required")
            dm.chat_needs_update = True
            win.write_event_value('-SUP-', 'CHAT')
        if (val['last_data_ts'] > dm.last_data_ts and not dm.data_needs_update):
            print("Data update required")
            dm.data_needs_update = True
            win.write_event_value('-SUP-', 'DATA')

        sleep(delay)

