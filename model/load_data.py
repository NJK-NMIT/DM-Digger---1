"""
Load all data from the remote server
"""

import model.network.jsn_drop_service as json



def load_data(dm) -> str:
    """Grab remote data and put it into the certs structure"""
    jsnDrop = json.jsnDrop()
    result = jsnDrop.all("dm_data")
    if "Data error" in result:
        if "Nothing selected" in result:
            dm.empty_certs()
            # Why the hell is 0 rows successfully returned an error?
            return("No data found.")
        else:
            # Don't wipe out any existing data when encountering an error,
            #   just report the error.
            oops = f"Error:\n{result}"
            print(oops)
            return(oops)

    dm.empty_certs()
    for row in result:
        cert = row["Cert_No"]
        type = row["App_Type"]
        date = row["App_Received"]
        month = date[:7]
        cnts = row["Appl_Contested"]
        name = row["Name"]
        if dm.DEBUG:
            print(f"Cert:{cert}\n  {name}\n  {type}\n  {date}\n  {month}\n  {cnts}")
        dm.certs['Cert_No'].append(name)
        dm.certs['App_Type'].append(type)
        dm.certs['App_Received'].append(month)
        dm.certs['Appl_Contested'].append(cnts)
        dm.certs['Name'].append(name)

    # Record the oldest and newest dates
    dates = sorted(dm.certs['App_Received'])
    dm.cert_min = dates[0]
    dm.cert_max = dates[-1]

    size = len(result)
    s = '' if size == 1 else "s"           
    return(f"{size} record{s} retrieved.")
