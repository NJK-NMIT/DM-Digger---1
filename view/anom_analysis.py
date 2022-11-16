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

    if not dm.certs["Name"]:
        return("No data loaded for Application Anomalies")

    view.View_dm.clear_previous_figure(dm)

    # Column that indicates an anomaly
    anom_column = "Appl_Contested"

    # Extract a list of the row indexes where something is anomalous
    indexes = [i for i,x in enumerate(dm.certs['Appl_Contested']) if x == "Yes"]

    if not indexes:
        return("No anomalies detected.")

    # Get all the names
    all_names = dm.certs["Name"]
    # Filter because we only those at the relavent indexes
    names = [ all_names[i] for i in indexes ]
    
    # Count the applications for each name
    # Note that it's likely there will be only 1 per name
    anom_dict = dict(Counter(names))

    names = anom_dict.keys()
    sizes = anom_dict.values()

    cnt = 0
    for i in sizes:
        cnt += i
    s = "ies"
    if cnt == 1:
        s = "y"
    view.View_dm.message_update(window, f"{cnt} anomal{s}.")

    fig = matplotlib.figure.Figure(figsize=(9, 3), dpi=100)
    fig.add_subplot(111).bar(names, sizes, color="blue")

    dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-ANOM-")
    return("")
