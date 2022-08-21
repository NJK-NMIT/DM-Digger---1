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

import PySimpleGUI as sg
import os.path
import pandas as pd


# Create a dictionary of constants rather than scatter them through the source
digger = { "in_file": "May-2022-Certificates.xlsx",
           "in_url":  "https://www.justice.govt.nz/assets/Documents/Publications/May-2022-Certificates.xlsx",
           "url_loc": "https://www.justice.govt.nz/tribunals/arla/register-of-licences-and-certificates/",
           "logo":    "DM Digger logo.png"
          }



#df = pd.read_excel(infile, sheet_name="Sheet1", header=1)
#
#df.head()
#print(df)

def load_local_excel():
    """
    Opens a file select dialogue

    Returns:
        string: the filename of the local file
    """
    pass

def load_remote_excel():
    """
    Pulls the excel file from the ARLA website and loads it

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
    exit_col = sg.Column([exit_button],element_justification='l')
    #info_col = sg.Column([info],element_justification='r')
    
    logo =  [ sg.Image(key="-LOGO-", filename=digger["logo"], size=(128,64), tooltip="Logo") ]
    debug = [ sg.Text('DEBg', size=(100,3), font='Any 12', key='-DEBUG-') ]
    info =  [ sg.Text('INFo', size=(100,4), font='Any 12', key='-INFO-') ]

    buttons = [ 
             sg.Button(f"Load Data", key='-LOAD-') ,
             sg.Button(f"Application\nFrequency", key='-FREQ-'),
             sg.Button(f"Application\nAnalysis", key='-ANAL-'),
             sg.Column(""),
             exit_col 
             ]

    data_img = [ sg.Image(key="-LOGO-", filename="Test.png", size=(500,260), tooltip="Data") ]

    left_column = [
                   logo,
                   info,
                   buttons 
                  ]


    right_column = [
                    debug,
                    data_img 
                   ]


    
    layout = [ 
            [ sg.Column(left_column),
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
    preconitions are met

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

    print(errors)
    return f"\n".join(errors)

   


if __name__ == "__main__":

    # Run the startup checks.  
    debug_text = run_startup_checks()

    # Create the application window. This is persistent until the application ends
    window = make_the_window()

    # Process window events until the window is closed or the Quit button is pressed
    while True:

        # Update the debug area with relavent info (even if blank)
        window['-DEBUG-'].update(debug_text)

        window['-DEBUG-'].update("DEBUGger")
        window['-INFO-'].update("INFOrmation")

        # Wait for a button to be clicked (or other action)
        event, values = window.read()


        if event == 'Quit' or event == sg.WIN_CLOSED:
            break

        debug_text = event



    kill_the_window(window)


