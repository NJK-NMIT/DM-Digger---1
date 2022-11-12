"""
Remove all data from the remote server
"""


import model.network.jsn_drop_service as json



def clear_data(dm) -> str:
    jsnDrop = json.jsnDrop()
    result = jsnDrop.delete("dm_data","1=1")
    if "Data error" in result:
        return(result)
    else:
        # Record the time we wiped out the data
        timestamp = dm.now()
        dm.set_data_timestamp(timestamp)
        return("All data removed.  You should load some new data now!")
