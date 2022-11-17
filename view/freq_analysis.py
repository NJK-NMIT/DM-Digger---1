"""
Process the frequency analysis element

"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from collections import Counter

matplotlib.use('TkAgg')

from model.Model_dm import Model_dm
import view.View_dm




def do_frequency_analysis(window, dm: Model_dm, values):
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

    # This is just here to suppress a warning.
    # values will always be passed in, even if we don't need it
    if values:
        pass

    # Mess about with the x axis formatting.  TODO: Make this work as intended.
    USE_X_SCALE = False
    
    if not dm.certs["Name"]:
        return("No data loaded for Frequency Analysis.")

    # Start with a clean slate
    view.View_dm.clear_previous_figure(dm)

    # Get the date values
    dates = sorted(dm.certs["App_Received"])
    # Filter them on the current date range (if a range is active)
    if dm.cert_min:
        dates = [ d for d in dates if d >= dm.cert_min and d <= dm.cert_max ]

    # How many in each month?
    sizes = dict(Counter(dates)).values()
    dates = list(set(dates))
    dates = sorted( [ dt.datetime.strptime(d,'%Y-%m').date() for d in dates ] )

    cnt = 0
    for i in sizes:
        cnt += i
    view.View_dm.message_update(window, f"{cnt} applications between {dm.cert_min} and {dm.cert_max}")

    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)

    if USE_X_SCALE:
        fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax = plt.gca()
        ax.set_xticklabels(ax.get_xticks(), rotation=45)


    fig.add_subplot(111).plot(dates, sizes)

    dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-FREQ-")
    return("")

