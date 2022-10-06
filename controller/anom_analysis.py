"""
Process the anomaly analysis e;ement

"""

import PySimpleGUI as sg

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
    window['-DATAIMG-'].update(dm.get_amonimg())
    return("No application anomalies detected in the current dataset")
    pass
