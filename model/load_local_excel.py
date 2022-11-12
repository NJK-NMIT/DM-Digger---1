"""
Deals with grabbing files from a local source.
"""

import re
import pandas as pd

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
    #   Timestamp('2020-03-10 00:00:00'    ->   2020-03-10
    for i in range(len(dm.certs['Cert_No'])):
        ts = str(dm.certs['App_Received'][i])
        date_pattern = '\d\d\d\d\-\d\d\-\d\d'
        dm.certs['App_Received'][i] = re.search(date_pattern, ts).group()
    
    # Send the certificate data over the network
    return( send_cert_data(dm) )


def send_cert_data(dm) -> str:

    max_threads = 5
    

    # Handle a single record
    def send_1_cert(cert) -> None:
        jsnDrop = json.jsnDrop()
        result = jsnDrop.store( "dm_data",[ cert ])
        if "Data error" in result:
            print(f"{result}\nError on:\n{cert}")
            quit()
        return None

 
    c = 0
    for i in range(len(dm.certs['Cert_No'])):
        cert = dm.certs["Cert_No"][i]
        send_1_cert( {
            "Cert_No":cert,
            "App_Type":dm.certs["App_Type"][i],
            "App_Received":dm.certs["App_Received"][i],
            "Appl_Contested":dm.certs["Appl_Contested"][i],
            "Name":dm.certs["Name"][i]
            } )
        c += 1

    return(f"{c} records successfully uploaded.")