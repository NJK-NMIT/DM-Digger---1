#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -q

""" 

DM Digger background information:
  DM Digger is an application designed to inspect the national register of
  alcohol Duty Managers in a user-friendly way.  The “Sale and Supply of
  Alcohol Act (2012)” created the requirement that a register
  “... recording all prescribed particulars relating to licences and
  managers' certificates” (SASAA 2012 §65) be set up and maintained. The
  act also required that this register be made available to the public.
  This was done via the periodic publication of certificate information via
  an excel spreadsheet. The spreadsheet is very basic and is merely a dump
  of certificate information.

Intended audience:
  The target users of the DM Digger application are those people appointed
  by the Medical Officer of Health (see References) who have a need to analyse
  information in the national register but lack the necessary skills in
  Microsoft Excel to do so.

Application purpose:
  The DM Digger application was created to make sense of the information in
  the published spreadsheet. It allows the user to interrogate the data to see
  which licensing authorities are processing the most applications and what part
  of the year has the most applications made. This allows the user to schedule
  their resources to the right part of the country at the right time of year.


"""

#from turtle import color
#from typing import Text
#import pandas as pd
import PySimpleGUI as sg
import os.path

# I'm legally required to include regular repression parsing in all programs
import re


# Create a dictionary of constants rather than scatter them through the source
digger = { "in_file":  "May-2022-Certificates.xlsx",
           "in_url":   "https://www.justice.govt.nz/assets/Documents/Publications/May-2022-Certificates.xlsx",
           "url_loc":  "https://www.justice.govt.nz/tribunals/arla/register-of-licences-and-certificates/",
           "logo":     "DM Digger logo.png",
           "Freq img": "Frequency example.png",
           "Appl img": "Application example.png",
           "Anom img": "Anomaly example.png"           
          }



def is_excel_filetype(filename):
    """
    Does the passed filename look like one of the (modernish) excel filetypes?

    TODO: Should probably check that the filetype is something pandas
          actually supports

    Args:
        string: A filename.
    Returns:
        Bool: If it looks like an excel file, return true.
              Otherwise return false
    """

    # We only care about the key.  The value data is just for completness
    ok = {
        ".xlsx": "Excel Workbook",
        ".xlsm": "Excel Macro-Enabled Workbook (code)",
        ".xlsb": "Excel Binary Workbook",
        ".xltx": "Template",
        ".xltm": "Template (code)",
        ".xls":	 "Excel 97- Excel 2003 Workbook",
        ".xlt":	 "Excel 97- Excel 2003 Template"
    }
    # Work out the filename extension and see if it's in the allowed list
    # While this whole subroutine could be done in one big (unreadable) regular
    #   expression, we're not coding in perl anymore :)
    ext = os.path.splitext(filename)[1]
    return ext in ok


def load_local_excel(filename):
    """
    Loads the passed filename as the dataset to be processed

    Args:
        string: The full path and filename of the excel file to load
    Returns:
        string: File processing status.
                Blank if no problems encountered.
                An error message if there was an issue.
    """
    #df = pd.read_excel(filename, sheet_name="Sheet1", header=1)
    #df.head()
    #print(df)
    if not is_excel_filetype(filename):
        return(f"{filename} is not an excel file")
    return("")
    pass


def load_remote_excel():
    """
    Pulls the excel file from the ARLA website and loads it

    Args:
        None.  The application knows where to find the ARLA data
    Returns:
        string: the URL of the excel file
    """
    pass


def make_the_window():
    """
    Creates the application window

    Returns:
        window: the handle to the application window
    """
    sg.theme('Light Grey 1')
    exit_button = [sg.Button('Quit', button_color = ('yellow','red'))]
    exit_col = sg.Column([exit_button], element_justification='l')
    
    logo = [ sg.Image(key="-LOGO-", filename=digger["logo"], size=(128,64), tooltip="Logo") ]
    debug = [ sg.Text('', size=(80,4), font='Any 12', key='-DEBUG-', background_color='white' ) ]
    info = [ sg.Text('', size=(30,2), font='Any 12', key='-INFO-', background_color='white') ]
    spacer = [ sg.Text('', size=(1,17), font='Any 12', key='-SPACER-') ]

    data_img = [ sg.Image(key="-DATAIMG-", filename="", size=(500,260), tooltip="Data") ]

    left_column = [
                   logo,
                   info,
                   [ sg.Button(f"Load Data", key='-LOAD-') ],
                   [ sg.Button(f"Application\nFrequency", key='-FREQ-') ],
                   [ sg.Button(f"Application\nAnalysis", key='-APPL-') ],
                   [ sg.Button(f"Application\nAnomalies", key='-ANOM-') ],
                   [ exit_col ],
                   spacer
                  ]

    right_column = [
                    debug,
                    data_img 
                   ]

    layout = [ 
            [ sg.Column(left_column, element_justification='l'),
              sg.VSeperator(),
              sg.Column(right_column) ]
            ]
    
    return  sg.Window('DM Digger', layout, size=(1280,600), finalize=True)


def kill_the_window(window):
    """
    Closes the window passed

    Args:
        window PySimpleGUI object: The handle of the window to be closed
    Returns:
        nothing

    """
    window.close()


def run_startup_checks():
    """
    Before the application main loop can start, we check that a set of
    preconitions are met.
    These are warnings rather than fatal errors.

    Returns:
        string: A list of failed checks.  An empty string if all checks are ok.

    """
    errors = []
    filename = digger['in_file']
    if os.path.exists(filename) != True:
        errors.append(f"Excel file '{filename}' not found")
    filename = digger['logo']
    if os.path.exists(filename) != True:
        errors.append(f"Logo file '{filename}' not found")
        digger['logo'] = ''
    filename = digger['Freq img']
    if os.path.exists(filename) != True:
        errors.append(f"Frequency image file '{filename}' not found")
    filename = digger['Appl img']
    if os.path.exists(filename) != True:
        errors.append(f"Application image file '{filename}' not found")
    filename = digger['Anom img']
    if os.path.exists(filename) != True:
        errors.append(f"Anomaly image file '{filename}' not found")

    return f"\n".join(errors)
    

def load_data_choice():
    """
    Loads data from a local excel file.
    No option for the remote fetch option yet.

    Args:
        None

    Returns:
        string: The filename of the selected file
    
    """
    layout = [[sg.Text("Choose a file: "), sg.FileBrowse(key='-IN-')], [sg.Button('Close', button_color = ('yellow','red'))]]
    sub_win = sg.Window('Data source', layout, size=(300,80), finalize=True)
    filename = ""

    while True:
        event, values = sub_win.read()
        if event == sg.WIN_CLOSED or event=="Close":
            filename = values['-IN-']
            break
    sub_win.close()
    return filename


def do_application_anomalies(window):
    """
    Reports on the non standard application.  Rejected, Needed puplic haring etc

    Args:
        The window filehandle

    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """
    window['-DATAIMG-'].update(digger["Anom img"])
    pass


def do_frequency_analysis(window):
    """
    Runs the frequency analysis algorythm on the loaded data. 
    Displays the result as a graph

    Args:
        The window filehandle

    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """
    window['-DATAIMG-'].update(digger["Freq img"])
    pass


def do_application_analysis(window):
    """
    Runs the frequency analysis algorythm on the loaded data. 
    Displays the result as a graph

    Args:
        The window filehandle

    Returns:
        string: Processing status
                Blank if no issue.
                Error text is problems encountered
    
    """
    window['-DATAIMG-'].update(digger["Appl img"])
    pass


def make_login_window():
    """
    Creates a login dialogue window.
    Username, password, submit.  You know.  The usual

    Returns:
        window: the handle to the login window
    """
    sg.theme('Light Grey 1')
    exit_button = [ sg.Button('Login', bind_return_key=True) ]
    exit_col = sg.Column( [exit_button], element_justification='l' )
    
    logo = [ sg.Image(key="-LOGO-", filename=digger["logo"], size=(128,64), tooltip="Logo") ]

    left_column = [
                logo,
                [sg.Text("Login:", size =(10, 1), font=16), sg.InputText(key='-username-', font=16, size=16)],
                [sg.Text("Password:", size =(10, 1), font=16), sg.InputText(key='-password-', font=16, size=16, password_char='*')],
                [ exit_col ],
                [ sg.Text('', size=(40,2), font='Any 12', key='-MESSAGE-', background_color='white' ) ]
                  ]

    layout = [ 
            [ sg.Column(left_column, element_justification='l')
               ]
            ]
    
    return  sg.Window('DM Digger login', layout, size=(480,200), finalize=True)



def is_password_valid(login, password):
    """
    Checks that the given login and password pair is valid.

    Args:
        string: A login name
        string: The (plaintext) password to check
    Returns:
        True/False: Is the given password the right one for the given login name
    """
    if login == "bob" and password == "x":
        return True
    else:
        return False



def get_login():
    """
    Continually asks for a valid login/password pair until either:
        A valid combo is entered.
        The login window is closed.

    Returns:
        string: The reserved word 'Quit' if the window was closed,
            otherwise the verified login name
    """
    login = ""
    error = ""
    window = make_login_window()

    # Keep reading the window input until a good login/password is encountered
    #   or the login window is closed.
    while True:
        event, values = window.read()

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

        window['-MESSAGE-'].update(error)


    kill_the_window(window)


    return(login)


if __name__ == "__main__":

    # Run the startup checks.  
    debug_text = run_startup_checks()

    # Get a login name
    login = ""
    while not login:
        login = get_login()
    if login == 'Quit':
        # The login window was closed so quit the application
        quit()

    # Create the application window. This is persistent until the application ends
    window = make_the_window()
    window['-INFO-'].update(f"Logged in as:\n  {login}")

    # Process window events until the window is closed or the Quit button is pressed
    while True:

        # Update the debug area with relavent info (even if blank)
        window['-DEBUG-'].update(debug_text)
        debug_text = ""

        # Wait for a button to be clicked (or other action)
        event, values = window.read()

        if event == '-LOAD-':
            data_file = load_data_choice()
            if data_file:
                debug_text = f"Input file set to {data_file}. Processing ..."
                window['-DEBUG-'].update(debug_text)
                # Replace the current dataset with data from the chosen file
                result = load_local_excel(data_file)
                # Strip the path from the datafile (for display purposes)
                data_file = os.path.split(data_file)[1]
                debug_text = f"Datafile {data_file} is processed {result}"
                # Only if loading is successful do we proceed.
                if len(result) == 0:
                    # When loading a new dataset, clear any previous result from the screen
                    window['-DATAIMG-'].update("")
                    # Let the user know what dataset is now active
                    window['-INFO-'].update(f"Using datafile:\n  {data_file}")
        elif event == '-FREQ-':
            do_frequency_analysis(window)
            debug_text = "Frequency Analysis"
        elif event == '-APPL-':
            do_application_analysis(window)
            debug_text = "Application Analysis"
        elif event == '-ANOM-':
            do_application_anomalies(window)
            debug_text = "No application anomalies detected in the current dataset"
        elif event == 'Quit' or event == sg.WIN_CLOSED:
            break
        else:
            debug_text = event



    kill_the_window(window)

