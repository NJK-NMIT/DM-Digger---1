"""
This is where the UI interaction lives

"""

import os.path
import PySimpleGUI as sg
import pandas as pd

from model.Model_dm import Model_dm
import view.View_dm
from model.access import is_password_valid


# Setup a dictionary of controlls for the view to populate
controlls = {}

def add_control(optn, func):
    """
    Adds a function handler for the given option.

    Args:
        string:  The name of the option.  Usually of the form "-NAME-"
        function name:  Self explanatory

    Returns:
        Nothing
    """

    # Complain and quit if the parameters are not of the right type
    if optn in controlls:
        print(f"Error: Option {optn} already exists")
        quit
    if not "func" in str(type(func)):
        print(f"Error: {func} is not a function")
        quit

    controlls[optn] = func



def process_events(window, dm):
    """
   Main loop.  Hand off events to the relavent function

    Args:
        Window handle:
        Model_dm object:

    Returns:
        Nothing
    """

    debug_text = ""

    # Process window events until the window is closed or the Quit button is pressed
    while True:

        # Update the debug area with relavent info from the last loop (even if blank)
        view.View_dm.debug_update(window, debug_text)
        debug_text = ""

        # Wait for a button to be clicked (or other action)
        event, values = window.read()

        # Loop through the controlls dictionary looking for event matches
        # Call the function of the matched event (if any)
        for control in controlls.keys():
            if event == control:
                debug_text = controlls[control](window, dm)

        if event == sg.WIN_CLOSED:
            break

    return("")



def data_choice_selector(win) -> str:
    """
   Handles the interaction for file selection

    Args:
        Window handle

    Returns:
        string: The filename of the selected file
    """
    filename = ""
    while True:
        event, values = win.read()
        if event == sg.WIN_CLOSED or event=="Close":
            filename = values['-IN-']
            break
    return(filename)



def login_window_selector(win) -> str:
    """
   Handles the interaction for the login screen

    Args:
        Window handle

    Returns:
        string: The login name of the successfylly logged in user.
                The "Quit" login is a special case that indicates the user
                    closed the login window without successfully logging in.
    """

    # Keep reading the window input until a good login/password is encountered
    #   or the login window is closed.
    login = ""
    error = ""
    while True:
        event, values = win.read()

        if event == "Login":
            login = values['-username-']
            passw = values['-password-']
            if is_password_valid(login, passw):
                break
            else:
                error = "Bad login/password"
        elif event == sg.WIN_CLOSED:
            login = 'Quit'
            break
        else:
            error = f"Undetected event: {event}"

        view.View_dm.message_update(win, error)
    
    return(login)


# Since quit isn't a function (it's a builtin) we need to create our own
#   function to quit.
# There may be arguments passed, we just dont care about them.
def just_quit(*args):
    quit()




def load_local_excel(filename, dm):
    """
    Loads the passed filename as the dataset to be processed

    Args:
        string: The full path and filename of the excel file to load
    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    if not dm.is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    df = pd.read_excel(filename, sheet_name="Sheet1", header=1)
    df.head(3)
    print(df)
    return("")




def merge_local_excel(filename, dm):
    """
    Takes the passed filename as the dataset to be merged with the current
        dataset.

    Args:
        string: The full path and filename of the excel file to load
    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    if not dm.is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    df = pd.read_excel(filename, sheet_name="Sheet1", header=1)
    df.head(6)
    print(df)
    return("")



def do_file_load(win, dm) -> str:
    """
   Load a new datafile

    Args:
        window: PSG object
        Model_dm object:

    Returns:
        string: The login name of the successfylly logged in user.
                The "Quit" login is a special case that indicates the user
                    closed the login window without successfully logging in.
    """
    data_file = view.View_dm.load_data_choice()
    if data_file:
        # Strip the path from the datafile (for display purposes)
        data_file_shortname = os.path.split(data_file)[1]
        debug_text = f"Input file set to {data_file_shortname}.\n\nProcessing ... (please wait) ... "
        view.View_dm.debug_update(win, debug_text)
        # PSG needs to poke to show the update since it can take ages to actually load the excel
        win.refresh()
        # Replace the current dataset with data from the chosen file
        result = load_local_excel(data_file, dm)
        debug_text = f"Processed {data_file_shortname}."
        view.View_dm.debug_update(win, debug_text)

        # Only if loading is successful do we proceed.
        if len(result) == 0:
            # When loading a new dataset, clear any previous result from the screen
            win['-DATAIMG-'].update("")
            # Let the user know what dataset is now active
            view.View_dm.info_update(win, f"Using datafile:\n  {data_file_shortname}")
        else:
            debug_text += f"Error: {result}"