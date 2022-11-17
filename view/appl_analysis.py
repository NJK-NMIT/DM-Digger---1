"""
Process the application analysis element

"""

from collections import Counter
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

from model.Model_dm import Model_dm
import view.View_dm




def do_application_analysis(window, dm: Model_dm, values):
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

    if not dm.certs["Name"]:
        return("No data loaded for Appllication Analysis.")

    view.View_dm.clear_previous_figure(dm)
 
    # Extract a list of the types, in the right date range
    types = [
        dm.certs['App_Type'][i] for i, x in enumerate(dm.certs['App_Received']) if x >= dm.cert_min and x <= dm.cert_max
        ]

    # Count the applications for each type
    app_types = sorted(types)
    app_types_dict = dict(Counter(app_types))
    # Data will looks something like:
    #   {'New Certificate': 123, 'Renew Certificate': 456, 'New Licence': 1}

    labels = app_types_dict.keys()
    sizes = app_types_dict.values()
    
    cnt = 0
    for i in sizes:
        cnt += i
    view.View_dm.message_update(window, f"{cnt} applications detected between {dm.cert_min} and {dm.cert_max}.")
    
    # Only graw a pie chart if we have data for one
    if cnt > 0:
        fig = matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
        fig.add_subplot(111).pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=45)
        dm.fig_canvas_agg = view.View_dm.draw_dm_figure(window['-CANVAS-'].TKCanvas, fig)

    dm.set_state("-APPL-")
    return("")

