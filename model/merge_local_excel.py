"""
Deals with merging a file from a local source

"""

import pandas as pd




def merge_local_excel(filename, dm) -> str:
    """
    Takes the passed filename as the dataset to be merged with the current
        dataset.

    Args:
        string: The full path and filename of the excel file to load
    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    if dm.frame.empty:
        return("No data to merge into.")

    if not dm.is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    df = pd.read_excel(filename, sheet_name="Sheet1", header=1)
    # To do the merge of dataframes, we simply glue them together and remove the duplicates.
    dm.frame = pd.concat([dm.frame, df])
    dm.frame.drop_duplicates(subset = ["Certificate Number"])

    return("")


