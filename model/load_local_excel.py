"""
Deals with grabbing files from a local source

"""

import pandas as pd




def load_local_excel(filename, dm):
    """
    Loads the passed filename as the dataset to be processed

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
    df.head(3)
    print(df)
    return("")
