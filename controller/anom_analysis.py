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


def __draw_dm_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



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
        return("No data loaded.")


    dm.set_state("-ANOM-")
    return("")
