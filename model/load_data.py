"""
Load all data from the remote server
"""

from model.Model_dm import Model_dm
import model.network.jsn_drop_service as json



def load_data(dm: Model_dm) -> str:
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
    dm.zoom_reset()

    for row in result:
        cert = row["Cert_No"]
        type = row["App_Type"]
        date = row["App_Received"]
        month = date[:7] # Only want the year and month (don't care if a day is supplied)
        cnts = row["Appl_Contested"]
        name = row["Name"]
        if dm.DEBUG_CERTIFICATES or len(date) != 7:
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

    # Build a list of all the months in the range
    # TODO: This is ugly as hell, make it pretty at some point.
    min_year, min_month = int(dm.cert_min[:4]), int(dm.cert_min[5:])
    max_year, max_month = int(dm.cert_max[:4]), int(dm.cert_max[5:])
    year, month = min_year, min_month
    dm.cert_range.append(f"{year:04}-{month:02}")
    while year*100 + month < max_year*100 + max_month:
        month += 1
        if month == 13:
            month = 1
            year += 1
        dm.cert_range.append(f"{year:04}-{month:02}")

    size = len(result)
    s = '' if size == 1 else "s"           
    return(f"{size} record{s} retrieved.\nRange: {dm.cert_min} to {dm.cert_max}")
