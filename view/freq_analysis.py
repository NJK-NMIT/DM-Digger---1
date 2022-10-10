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




def do_frequency_analysis(window, dm):
    """
    Runs the frequency analysis algorythm on the loaded data. 
    Displays the result as a graph

    Args:
        The window filehandle
        Model_dm object

    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """
    
    if dm.frame.empty:
        return("No data loaded for Frequency Analysis.")

    view.View_dm.clear_previous_figure(dm)


    # Which column the dates are in
    dkey = "Date Application was Received"
    # New column name for the truncated dates
    mkey = "Month"

    # Only interested in the month component of a date
    dm.frame[mkey] = dm.frame[dkey].astype("datetime64[M]")
    # Make sure they are in date order
    dm.frame = dm.frame.sort_values(by=mkey)

    # Count the applications for each month
    app_types = dm.frame[mkey].tolist()
    app_types_dict = dict(Counter(app_types))

    dates = app_types_dict.keys()
    sizes = app_types_dict.values()

    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    fig.add_subplot(111).plot(dates, sizes)

    dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-FREQ-")
    return("")

