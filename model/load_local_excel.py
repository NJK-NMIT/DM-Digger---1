"""
Deals with grabbing files from a local source

"""

import pandas as pd




def load_local_excel(filename, dm) -> str:
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
