"""
Process the frequency analysis element

"""

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use('TkAgg')

from collections import Counter


from model.Model_dm import Model_dm
import view.View_dm




def do_frequency_analysis(window, dm, values):
    """
    Runs the frequency analysis algorythm on the loaded data. 
    Displays the result as a graph

    Args:
        The window filehandle
        Model_dm object
        window values


    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """
    
    if not dm.certs["Name"]:
        return("No data loaded for Frequency Analysis.")

    view.View_dm.clear_previous_figure(dm)


    """
    # New column name for the truncated dates
    mkey = "Month"

    # Only interested in the month component of a date
    dm.frame[mkey] = dm.frame[dkey].astype("datetime64[M]")
    # Make sure they are in date order
    dm.frame = dm.frame.sort_values(by=mkey)

    # Count the applications for each month
    app_types = dm.frame[mkey].tolist()
    app_types_dict = dict(Counter(app_types))
    """

    # Get the date values
    dates = sorted(dm.certs["App_Received"])
    # How many in each month?
    sizes = dict(Counter(dates)).values()
    dates = list(set(dates))

    cnt = 0
    for i in sizes:
        cnt += i
    view.View_dm.message_update(window, f"{cnt} applications.")

    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    fig.add_subplot(111).plot(dates, sizes)

    dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-FREQ-")
    return("")

