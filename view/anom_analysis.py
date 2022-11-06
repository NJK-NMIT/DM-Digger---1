"""
Process the anomaly analysis element

"""

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

matplotlib.use('TkAgg')

from collections import Counter


from model.Model_dm import Model_dm
import view.View_dm





def do_application_anomalies(window, dm, values):
    """
    Reports on the non standard application.  Rejected, Needed puplic hearing etc

    Args:
        The window filehandle
        Model_dm object
        window values

    Returns:
        string: Processing status
                Blank if no issue.
                Error text if problems encountered
    
    """

    if dm.frame.empty:
        return("No data loaded for Application Anomalies")

    view.View_dm.clear_previous_figure(dm)

    # Which column the dates are in
    dkey = "Date Application was Received"
    # Column that indicates an anomaly
    anom_column = "Application Contested"

    # Extract only the rows where something is anomalous
    tmp = dm.frame.loc[dm.frame[anom_column] == 'Yes']

    # Which column the dates are in
    dkey = "Certificate Holder's First Names"

    # Count the applications for each name
    # Note that it's likely there will be only 1 per name
    app_types = tmp[dkey].tolist()
    app_types_dict = dict(Counter(app_types))

    dates = app_types_dict.keys()
    sizes = app_types_dict.values()

    cnt = 0
    for i in sizes:
        cnt += i
    s = "ies"
    if cnt == 1:
        s = "y"
    view.View_dm.message_update(window, f"{cnt} anomal{s}.")

    fig = matplotlib.figure.Figure(figsize=(9, 3), dpi=100)
    fig.add_subplot(111).bar(dates, sizes, color="blue")

    dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-ANOM-")
    return("")
