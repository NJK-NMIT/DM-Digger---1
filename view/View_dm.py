"""
This is where the UI stuff for DM Digger belongs

"""

import PySimpleGUI as sg
#from model.Model_dm import Model_dm


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
    window['-DATAIMG-'].update(dm.get_freqimg())
    pass




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
    pass


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
    window['-DATAIMG-'].update(dm.get_amonimg())
    pass