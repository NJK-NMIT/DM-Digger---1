"""
Process the application analysis element

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


def do_application_analysis(window, dm):
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
        return("No data loaded.")

    # Clear any previous figure
    plt.close('all')

    # Count the applicatoins for each type
    app_types = dm.frame['Application Type'].tolist()
    app_types_dict = dict(Counter(app_types))
    # Data will looks something like:
    #   {'New Certificate': 123, 'Renew Certificate': 456, 'New Licence': 789}

    labels = app_types_dict.keys()
    sizes = app_types_dict.values()

    fig = matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
    fig.add_subplot(111).pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=45)

    fig_canvas_agg = __draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-APPL-")
    return("")

