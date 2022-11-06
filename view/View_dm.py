"""
This is where the UI stuff for DM Digger belongs

"Now these points of data make a beautilful line ...."
"""

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from model.Model_dm import Model_dm
import matplotlib.pyplot as plt
import controller.Controller_dm
import controller.chat
import view.freq_analysis
import view.appl_analysis
import view.anom_analysis
import lyfe.PyLyfe as lyfe


def refresh(win):
    """
    Force a display update of the given window

    Args:
        Window object:

    Returns:
        Nothing
    """
    win.refresh()


def make_the_window(dm):
    """
    Creates the application window

    Args:
        Model_dm object:

    Returns:
        window: the handle to the application window
    """
    sg.theme('Light Grey 1')

    # Start by defining the exit button and its controller
    exit_button = [sg.Button('Quit', button_color = ('yellow','red'))]
    controller.Controller_dm.add_control('Quit', controller.Controller_dm.just_quit)
    exit_col = sg.Column([exit_button], element_justification='l')
    
    # Cosmetic elements
    logo = [ sg.Image(key="-LOGO-", filename=dm.get_logo(), size=(128,64), tooltip="Logo") ]
    debug = [ sg.Text('', size=(80,4), font='Any 12', key='-DEBUG-', background_color='white' ) ]
    message = [ sg.Text('', size=(80,2), font='Any 12', key='-MESSAGE-', background_color='white' ) ]
    info = [ sg.Text('', size=(30,2), font='Any 12', key='-INFO-', background_color='white') ]
    spacer = [ sg.Text('', size=(1,17), font='Any 12', key='-SPACER-') ]

    # A canvas for the image/plot
    data_plot = [ sg.Canvas(key='-CANVAS-') ]

    # Add an easter egg.  A blank button, the same size as Quit, which runs Conway's game of life
    egg_button = [sg.Button('      ', button_color = ('yellow','white'))]
    controller.Controller_dm.add_control('      ', lyfe.start_lyfe_thread)
    egg_col = sg.Column([egg_button], element_justification='l')

    # The chat interface
    chatbox   = [ sg.Text('Empty chat', size=(80,4), font='Any 12', key='-CHATTEXT-', background_color='lightgrey' ) ]
    chatinput = [ sg.Input('Say something ...',  do_not_clear=False, key="-CHATSEND-"),
                  sg.Button('Submit', visible=True, bind_return_key=True) ]
    controller.Controller_dm.add_control('Submit', controller.chat.send)



    # Place the logo, the buttons, etc, as the LHS of the window
    left_column = [
                   logo,
                   info,
                   [ sg.Button(f"Load Data", key='-LOAD-') ],
                   [ sg.Button(f"Merge Data", key='-MERGE-') ],
                   [ sg.Button(f"Application\nFrequency", key='-FREQ-') ],
                   [ sg.Button(f"Application\nAnalysis", key='-APPL-') ],
                   [ sg.Button(f"Application\nAnomalies", key='-ANOM-') ],
                   [ exit_col ],
                   [ egg_col ],
                   spacer
                  ]

    # Add actions for each button
    controller.Controller_dm.add_control('-LOAD-',  controller.Controller_dm.do_file_load)
    controller.Controller_dm.add_control('-MERGE-', controller.Controller_dm.do_file_merge)
    controller.Controller_dm.add_control('-FREQ-',  view.freq_analysis.do_frequency_analysis)
    controller.Controller_dm.add_control('-APPL-',  view.appl_analysis.do_application_analysis)
    controller.Controller_dm.add_control('-ANOM-',  view.anom_analysis.do_application_anomalies)

    # The RHS of the window is all output elements
    right_column = [
                    chatbox, chatinput,
                    debug,
                    message,
                    data_plot
                   ]

    # Join the 2 sides together
    layout = [ 
            [ sg.Column(left_column, element_justification='l'),
              sg.VSeperator(),
              sg.vtop(sg.Column(right_column))
            ]
             ]
    
    return sg.Window('DM Digger', layout, size=(1280,600), finalize=True)


def info_update(window, message):
    """
    Updates the "Info" UI element with the given message

    Args:
        window PySimpleGUI object: The handle of the window to be closed
        string: words to display

    Returns:
        Nothing
    """
    window['-INFO-'].update(message)



def debug_update(window, message):
    """
    Updates the "Debug" UI element with the given message

    Args:
        window PySimpleGUI object: The handle of the window to be closed
        string: words to display

    Returns:
        Nothing
    """
    window['-DEBUG-'].update(message)
    refresh(window)


def message_update(window, message):
    """
    Updates the "Message" UI element with the given message

    Args:
        window PySimpleGUI object: The handle of the window to be closed
        string: words to display

    Returns:
        Nothing
    """
    window['-MESSAGE-'].update(message)
    refresh(window)



def load_data_choice(message) -> str:
    """
    A file selector for a local excel file.
    No option for the remote fetch option yet.

    Args:
        message: string.  A message to print at the top of the screen

    Returns:
        string: The filename of the selected file
    """
    layout = [
        [sg.Text(message)],
        [sg.Text("Choose a file: "), sg.FileBrowse(key='-IN-')],
        [sg.Button('Open', button_color = ('yellow','red'))]
        ]
    sub_win = sg.Window('Data source', layout, size=(400,120), finalize=True)

    filename = controller.Controller_dm.data_choice_selector(sub_win)

    sub_win.close()
    return filename






def kill_the_window(window):
    """
    Closes the window passed

    Args:
        window PySimpleGUI object: The handle of the window to be closed
    Returns:
        nothing

    """
    window.close()



def make_login_window(dm):
    """
    Creates a login dialogue window.
    Username, password, submit.  You know.  The usual

    Returns:
        window: the handle to the login window
    """
    sg.theme('Light Grey 1')
    exit_button = [ sg.Button('Login', bind_return_key=True) ]
    exit_col = sg.Column( [exit_button], element_justification='l' )
    
    logo = [ sg.Image(key="-LOGO-", filename=dm.get_logo(), size=(128,64), tooltip="Logo") ]

    left_column = [
                logo,
                [sg.Text("Login:", size=(10, 1), font=16), sg.InputText(key='-username-', font=16, size=16)],
                [sg.Text("Password:", size=(10, 1), font=16), sg.InputText(key='-password-', font=16, size=16, password_char='*')],
                [ exit_col ],
                [ sg.Text('', size=(40,2), font='Any 12', key='-MESSAGE-', background_color='white' ) ]
                  ]

    layout = [ 
            [ sg.Column(left_column, element_justification='l')
               ]
            ]
    
    return  sg.Window('DM Digger login', layout, size=(480,200), finalize=True)



def get_login(dm):
    """
    Continually asks for a valid login/password pair until either:
        A valid combo is entered.
        The login window is closed.
    Args:
        Model_dm object:

    Returns:
        string: The login of the successfully logged in user
    """
    window = make_login_window(dm)
    login = controller.Controller_dm.login_window_selector(window)
    dm.set_login(login)
    # Don't leave the login window hanging around!
    kill_the_window(window)

    return(login)


def clear_previous_figure(dm):
    # Clear any previous figure
    # Example from class to emulate: self.figure_agg.get_tk_widget().forget()
    if dm.fig_canvas_agg:
        dm.fig_canvas_agg.get_tk_widget().forget()
        plt.close('all')



def draw_dm_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
