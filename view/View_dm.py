"""
This is where the UI stuff for DM Digger belongs

"Now these points of data make a beautilful line ...."
"""

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from model.Model_dm import Model_dm
import model.load_data
import matplotlib.pyplot as plt
import controller.Controller_dm
import controller.chat
import view.freq_analysis
import view.appl_analysis
import view.anom_analysis
import controller.chat
import controller.zoom


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


def make_the_window(dm: Model_dm):
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
    info = [ sg.Text('', size=(30,3), font='Any 12', key='-INFO-', background_color='white') ]
    spacer = [ sg.Text('', size=(1,17), font='Any 12', key='-SPACER-') ]
    # Supervisor events can get notified here.  Do we really need an element to post to?
    sup_notify = [ sg.Text('', size=(4,1), font='Any 12', key='-SUP-', background_color='white') ]

    # A canvas for the image/plot
    data_plot = [ sg.Canvas(key='-CANVAS-') ]

    # Add an easter egg.  A blank button, the same size as Quit, which runs Conway's Game of Life
    egg_button = [sg.Button('      ', button_color = ('yellow','white'))]
    controller.Controller_dm.add_control('      ', lyfe.start_lyfe_thread)
    egg_col = sg.Column([egg_button], element_justification='l')

    # The chat interface
    chatbox   = [ sg.Multiline('Empty chat', size=(80,4), font='Any 12',
                  key='-CHATTEXT-', background_color='lightgrey', autoscroll=True ) ]
    chatinput = [ sg.Input('Say something ...',  size=(60, 1), do_not_clear=False, key="-CHATSEND-", font='Any 16'),
                  sg.Button('Submit', visible=True, font='Any 12', bind_return_key=True) ]
    controller.Controller_dm.add_control('Submit', controller.chat.send)

    # Focus and Zoom stuff
    range = [ sg.Text('Working date range:', size=(38,1), font='Any 12', key='-RANGE-', background_color='white') ]
    size_text = [ sg.Text('Date size:', size=(11,1), font='Any 12', background_color='white') ]
    pos_text = [ sg.Text('Date position:', size=(15,1), font='Any 12', background_color='white') ]

    zoom =  [ sg.Slider(range=(1, 100), orientation='h', size=(25, 20),
              default_value=100, key='-ZOOM-', enable_events = True) ]
    controller.Controller_dm.add_control('-ZOOM-', controller.zoom.zoom)
    focus =  [ sg.Slider(range=(1, 100), orientation='h', size=(25, 20),
              default_value=50, key='-FOCUS-', enable_events = True) ]
    controller.Controller_dm.add_control('-FOCUS-', controller.zoom.focus)




    # Place the logo, the buttons, etc, as the LHS of the window
    left_column = [
                   logo,
                   info,
                   [ sg.Button(f"Load Data", key='-LOAD-') ],
                   [ sg.Button(f"Clear Data", key='-CLEAR-') ],
                   [ sg.Button(f"Application\nFrequency", key='-FREQ-') ],
                   [ sg.Button(f"Application\nAnalysis", key='-APPL-') ],
                   [ sg.Button(f"Application\nAnomalies", key='-ANOM-') ],
                   [ exit_col ],
                   [ egg_col ],
                   range, size_text, zoom, pos_text, focus,
                   sup_notify, spacer
                  ]

    # Add actions for each button
    controller.Controller_dm.add_control('-LOAD-',  controller.Controller_dm.do_file_load)
    controller.Controller_dm.add_control('-CLEAR-', controller.Controller_dm.do_data_clear)
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
    
    return sg.Window('DM Digger', layout, size=(1280,700), finalize=True)


def range_update(window, message: str) -> None:
    """Updates the 'range' text element"""
    window['-RANGE-'].update(message)


def info_update(window, message: str):
    """
    Updates the "Info" UI element with the given message

    Args:
        window PySimpleGUI object: The handle of the window to be closed
        string: words to display

    Returns:
        Nothing
    """
    window['-INFO-'].update(message)



def debug_update(window, message: str):
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


def message_update(window, message: str):
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



def load_data_choice(message: str) -> str:
    """
    A file selector for a local excel file.
    No option for the remote fetch option yet.

    Args:
        message: string.  A message to print at the top of the screen

    Returns:
        string: The filename of the selected file
    """
    # TODO: Opening the file browser cause these error message to come from the supervisor thread 
    #       +[CATransaction synchronize] called within transaction
    #       We need to add a flag here to tell the supervisor to pause for a bit.
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



def make_login_window(dm: Model_dm):
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



def get_login(dm: Model_dm):
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


def clear_previous_figure(dm: Model_dm):
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




def show_chat(win, dm: Model_dm) -> None:
    max_chats = 50
    # Get the chat message from the networks and display them
    chats = controller.chat.fetch()

    # Only look at the last X chats (at most).
    show_chat = chats[-max_chats:]

    # If we have more chats in the DB than we care about, delete them from the DB.
    if len(chats) > len(show_chat):
        # Remove everything older than the first one we're showing
        controller.chat.remove_old_chats(show_chat[0]["Timestamp"])

    # Format the list for human readability
    chat_text, last_ts = "", ""
    for row in show_chat:
        chat_text += f"{row['User_ID']}: {row['Message']}\n"
        last_ts = row["Timestamp"]
    win['-CHATTEXT-'].update(chat_text)
    refresh(win)

    # We just updated the chat display
    dm.chat_needs_update = False
    # Record the timestamp of the last shown chat message
    dm.last_chat_ts = last_ts





def show_data_load(win, dm: Model_dm) -> None:

    debug_update(win, "Loading network data.  Please wait ...")

    # Get the data from the network
    result = model.load_data.load_data(dm)
    info_update(win, result)

    # We just fetched the data.  Inidcate that
    dm.data_needs_update = False
    dm.last_data_ts = dm.now()
