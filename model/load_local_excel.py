"""
Deals with grabbing files from a local source.
"""

import re
import threading
import pandas as pd
import time

import model.network.jsn_drop_service as json




def load_local_excel_to_frame(filename, dm) -> str:
    """
    Loads the passed filename as the dataset to be processed
    Adds a pandas dataframe to the "frame" element
    
    Args:
        string: The full path and filename of the excel file to load

    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    if not dm.is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    df = pd.read_excel(filename, sheet_name="Sheet1", header=1)
    dm.frame = df
    return("")



def load_local_excel_internal(filename, dm) -> str:
    """
    Loads the passed filename as the dataset to be processed
    Populates the "certs" element of object
    
    Args:
        string: The full path and filename of the excel file to load

    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    if not dm.is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    df = pd.read_excel(filename, sheet_name="Sheet1", header=1)

    # Start with an empty list of certificates
    dm.empty_certs()

    # This is the mapping from the DB columns to the dictionary keys
    keymapping = {
        "Cert_No":        'Certificate Number',
        "App_Type":       'Application Type',
        "App_Received":   'Date Application was Received',
        "Appl_Contested": 'Application Contested',
        "First_Names":     "Certificate Holder's First Names",
        "Last_Name":       "Certificate Holder's Last Name"
    }
    # Perform the mapping
    for key, value in keymapping.items():
        # Mapping {value} to {key}
        dm.certs[key] = df[value].tolist()
    # Create the "Name" data
    for i in range(len(dm.certs['Cert_No'])):
        name = dm.certs['First_Names'][i] + dm.certs['Last_Name'][i]
        # Regex is to make sure the name contains no double spaces
        dm.certs['Name'].append( re.sub(' +', ' ', name) )
    # Eliminate the unnecessary keys
    del dm.certs['First_Names']
    del dm.certs['Last_Name']
    # Clean up the timestamps
    #   Timestamp('2020-03-10 00:00:00'    ->   2020-03
    for i in range(len(dm.certs['Cert_No'])):
        ts = str(dm.certs['App_Received'][i])
        date_pattern = '\d\d\d\d\-\d\d'
        dm.certs['App_Received'][i] = re.search(date_pattern, ts).group()
    
    # Send the certificate data over the network
    return( send_cert_data_threads(dm) )




def send_cert_data_threads(dm) -> str:
    """Load the existing certificate data via JSON.  Uses a LOT of threads."""

    THREAD_DEBUG = False
    # 200 looks like it will always produce "Max retries exceeded" errors :(
    # 150 looks like it will sometimes produce "Max retries exceeded" errors :(
    max_threads = 111

    # Handle a single record
    # TODO: Sending more than one record in a single JSON - How many is safe?
    def send_1_cert_t(cert) -> None:
        jsnDrop = json.jsnDrop()
        result = jsnDrop.store( "dm_data", [cert])
        if "Data error" in result:
            print(f"{result}\nError on:\n{cert}")
        return None
 
    # Keep a count of how many we upload
    i = 0
    # Hold a list of active threads
    threads = []
    # We want to know how long the total upload time was
    start_time = time.monotonic()

    # We build a list of integers, one for each certificate,
    #   and slowly destroy it until there is nothing left.
    s = list( range(len(dm.certs['Cert_No'])) )
    while s:
        t_id = s.pop(0)
        cert_id = dm.certs["Cert_No"][i]
        cert = {
            "Cert_No":cert_id,
            "App_Type":dm.certs["App_Type"][i],
            "App_Received":dm.certs["App_Received"][i],
            "Appl_Contested":dm.certs["Appl_Contested"][i],
            "Name":dm.certs["Name"][i]
            }
        if THREAD_DEBUG:
            print(f"Sending {cert_id} on thread {t_id} / {len(threads)}")
        p = threading.Thread( target=send_1_cert_t, args=(cert,) )
        p.start()
        threads.append(p)
        # If we're maxed out on threads, wait for the earliest to finish
        if len(threads) >= max_threads:
            t = threads.pop(0)
            t.join()
        i += 1

    # Wait on all the remaining threads to complete
    while threads:
        t = threads.pop(0)
        t.join()

    # Record the time we finished writing.
    # This lets all processes, including ourself, know that there is "new" data available
    dm.set_data_timestamp( dm.now() )

    duration = round(time.monotonic() - start_time, 1)
 
    return(f"{i} records uploaded in {duration} seconds.")
