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





def do_application_anomalies(window, dm):
    """
    Reports on the non standard application.  Rejected, Needed puplic hearing etc

    Args:
        The window filehandle
        Model_dm object

    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """

    if dm.frame.empty:
        return("No data loaded for Application Anomalies")

    view.View_dm.clear_previous_figure(dm)


    dm.set_state("-ANOM-")
    return("")
