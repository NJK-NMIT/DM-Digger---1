"""
Process the application analysis e;ement

"""

import PySimpleGUI as sg

from model.Model_dm import Model_dm
import view.View_dm


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
    window['-DATAIMG-'].update(dm.get_applimg())
    return("Application Analysis")
    pass


