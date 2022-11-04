#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -q

"""
PyLyfe
  This is a training excerise to help me learn graphical python


"""


import PySimpleGUI as sg
import os.path
import random
import time
import copy
import threading


field = []
need_update = []
f_rows = 20   # 27 is good for cell_size 8
f_cols = 42   # 52 is good for cell_size 8
cell_size = 14
new_pct = 7
f_on   = 'grey'
f_off  = 'white'

show_neighbour_count = False
show_survivors = False


# Store the thread object for running generations.
# Only one thread for generation processing!
the_thread = None


def make_the_window():
    """
    Creates the application window

    Returns:
        window: the handle to the application window
    """
    sg.theme('Light Grey 1')
    exit_button = [sg.Button('Quit', button_color = ('yellow','red'))]
    step_button = [sg.Button('Step')]
    stop_button = [sg.Button('Stop')]
    more_button = [sg.Button('Add cells')]
    run_button  = [sg.Button('Run')]
    fast_button = [sg.Button('Run Fast')]
    cls_button  = [sg.Button('Clear')]
    lodup_button = [sg.Button('Up glider')]
    loddn_button = [sg.Button('Down glider')]

    lod1_button = [sg.Button('Load growth')]
    left_button = [sg.Button('Left glider')]
    lod4_button = [sg.Button('Interesting')]
    lod5_button = [sg.Button('Massive glider')]
    lod7_button = [sg.Button('3 cycle')]

    show_cnt_button = [sg.Button('Show neighbours', button_color = ('white','blue'))]
    show_surv_button = [sg.Button('Show survivors', button_color = ('white','blue'))]

    exit_col = sg.Column([exit_button], element_justification='l')

    # Logo taken from: https://www.facebook.com/pythonlife/photos/124228609281039
    logo = [ sg.Image(key="-LOGO-", filename="lyfe/Logo.png", size=(128,128), tooltip="Logo") ]
    debug = [ sg.Text('', size=(20,4), font='Any 12', key='-DEBUG-' ) ]

    # Something
    run_buttons  = sg.Column([ run_button, step_button, stop_button, more_button, cls_button ])
    load_buttons = sg.Column([ lod1_button, lodup_button, loddn_button, left_button,
        lod4_button, lod5_button, lod7_button ])
    extra_buttons = sg.Column([ show_cnt_button, show_surv_button ])

    # Left column is info/control
    left_column = [
                   logo,
                   debug,
                   [ run_buttons ],
                   [ load_buttons ],
                   [ exit_col ],
                   [ extra_buttons ]
                  ]

    # Right column is the playing field
    right_column = []
    for row in range (0, f_rows):
       right_column += [[sg.Text(" ",
                        key=f"-{str(row*100+col).zfill(4)}-",
                        size=1, font=f"Any {cell_size}",
                        # Tooltips are nice for debugging but slow the display down
#                        tooltip=f"{str(row*100+col).zfill(4)}",
                        background_color=f_off) for col in range(0, f_cols)]
                        ]

    layout = [
            [ sg.Column(left_column, justification='l', vertical_alignment='t'),
              sg.VSeperator(),
              sg.Column(right_column) ]
            ]

    return  sg.Window('PyLyfe', layout, size=(1320,680), finalize=True, element_justification='l')


def force_all_update():
    """
    Flag that we need all cells to get a display update

    The need_update is a set of flags to indicate if that cell has changed in the last round
    """
    global need_update
    need_update = []
    for row in range (0, f_rows):
        need_update += [[True for col in range(0, f_cols)]]



def make_the_field():
    """
    We build the initial (blank) field here
    The field is an array of arrays (of all the same size)
    """
    global field
    field = []
    for row in range (0, f_rows):
        field += [[False for col in range(0, f_cols)]]
    force_all_update()


def toggle_neighbours():
    global show_neighbour_count
    show_neighbour_count = not show_neighbour_count
    force_all_update()

def toggle_survivors():
    global show_survivors
    show_survivors = not show_survivors
    force_all_update()


def load_pattern_up_glider():
    pattern = [[True, True, True], [True, False, False], [False, True, False]]
    load_pattern(pattern)

def load_pattern_1():
    pattern = [[False, True, True], [True, True, False], [False, True, False]]
    load_pattern(pattern)

def load_pattern_2():
    pattern = [[False, False, True], [True, False, True], [False, True, True]]
    load_pattern(pattern)

def load_pattern_left():
    pattern = [ [False, False, True, True, False],
                [False, True, True, True, True],
                [True, True, False, True, True],
                [False, True, True, False, False]]
    load_pattern(pattern)

def load_pattern_4():
    map=""".OOO...........OOO
O..O..........O..O
...O....OOO......O
...O....O..O.....O
..O....O........O."""
    pattern = load_map(map)
    load_pattern(pattern)

def load_pattern_5():
    map = """..........OO...............
.....OOO..OOO..............
.......O..OO.O.O....O......
.....OO.....OOO......O.....
.OO..O..OOO.O...OOOO.O....O
OO.OO.....O....OO...OOO.O.O
.O...O.........O........O.O
OO...O.....................
.O...O.........O........O.O
OO.OO.....O....OO...OOO.O.O
.OO..O..OOO.O...OOOO.O....O
.....OO.....OOO......O.....
.......O..OO.O.O....O......
.....OOO..OOO..............
..........OO..............."""
    pattern = load_map(map)
    load_pattern(pattern)

# A 540 generation loop!
# Argh! But what was the screen resolution to get this?
def load_pattern_6():
    map = """OOO...........OOO.
O..O..........O..O
O......OOO....O...
O.....O..O....O...
.O.O..O...O....O.O
.......OOOO.......
.........O........
..................
..................
..................
.......OOO........
.......O..........
........O........."""
    pattern = load_map(map)
    load_pattern(pattern)

# The pulsar
def load_pattern_7():
    map = """..OOO...OOO..
.............
O....O.O....O
O....O.O....O
O....O.O....O
..OOO...OOO..
.............
..OOO...OOO..
O....O.O....O
O....O.O....O
O....O.O....O
.............
..OOO...OOO.."""
    pattern = load_map(map)
    load_pattern(pattern)



def load_map(map):
    pattern = []
    for line in map.split("\n"):
        p_line = []
        for char in line:
            if char == ".":
                p_line.append(False)
            elif char == "O":
                p_line.append(True)
        pattern.append(p_line)
    return(pattern)


def load_pattern(pattern):
    """
    Overlay a pattern on the field
    """
    offset = 3
    r = 0
    global need_update
    for row in pattern:
        c = 0
        for cell in row:
            field[offset+r][offset+c] = cell
            need_update[offset+r][offset+c] = True
            c += 1
        r += 1



def randomise_the_field(pct):
    """
    For each cell, randomly set it to True

    Args:
        integer: Percentage change that a field will be set
    Returns:
        nothing
    """
    global field
    global need_update
    for row in range (0, f_rows):
        for col in range (0, f_cols):
            if random.randint(0, 99) < pct:
                field[row][col] = True
                need_update[row][col] = True


def show_the_field(window):
    """
    Display the whole field by updating the window's cells
    """
    global field
    global need_update
    for row in range (0, f_rows):
        for col in range (0, f_cols):
            cell = f"-{str(row*100+col).zfill(4)}-"
            if need_update[row][col] is True:
                need_update[row][col] = False
                if field[row][col] is True:
                    window[cell].update(background_color=f_on)
                else:
                    window[cell].update(background_color=f_off)
            else:
                pass
                # Set cells that lived through the last generation to blue
                if show_survivors:
                    if field[row][col] is True:
                        window[cell].update(background_color='blue')

#           # We can show the neighbour count on the cell if we want
            if show_neighbour_count:
                nbrs = get_neighbours(row, col) or " "
                window[cell].update(nbrs)
            else:
                # TODO: This needs optomised.  Most of the time it is unnecessary 
                window[cell].update(" ")
                



def get_neighbours(row, col):
    global field
    cnt = 0
    # Loop over our immediate neighbours.
    # That is cells immediately above, below and to the left and right.
    # We include the cells in the upleft, downright, etc, positions.
    for l_row in [-1, 0, 1]:
        for l_col in [-1, 0, 1]:
            # Don't count ourself
            if not (l_row == l_col == 0):
                # %f_xxxx is to allow for warping to the other side of the field
                x = (row + l_row + f_rows) % f_rows
                y = (col + l_col + f_cols) % f_cols
                if field[x][y] is True:
                    cnt += 1
    return cnt



def do_a_single_generation():
    """Execute the "lyfe" rules for a single cycle.
    Rules are applied to all cells simultaneously

    Args:
        None
    Returns:
        nothing

    All updates are performed on the global field; No display changes are performed.
    """
    global field
    newfield = copy.deepcopy(field)
    for row in range (0, f_rows):
        for col in range (0, f_cols):
            # How many neighbours do we have?
            nbrs = get_neighbours(row, col)
            # If we're alive, stay alive only if we have 2 or 3 neighbours
            if field[row][col] is True:
                if nbrs not in (2, 3):
                    newfield[row][col] = False
                    need_update[row][col] = True
            # If we're dead and have 3 neighbours, make us alive!
            elif nbrs == 3:
                newfield[row][col] = True
                need_update[row][col] = True
    field = newfield


def kill_the_window(window):
    """
    Closes the window passed

    Args:
        window PySimpleGUI object: The handle of the window to be closed
    Returns:
        nothing

    """
    window.close()


def get_current_hash():
    """
    Create a hash value for the current field
    """
    thing = ""
    for row in range (0, f_rows):
        for col in range (0, f_cols):
            if field[row][col] is True:
                thing += "a"
            else:
                thing += "b"
    return hash(thing)


def stop_generation():
    global the_thread
    the_thread = None


def run_lyfe_thread(window, **kwargs):
    """
    A threaded version of the run_lyfe routine.
    This version though ...
    Returns:
        Thread object
    """
    global the_thread
    if the_thread is None:
        return threading.Thread(target=run_lyfe, args=(window, ), kwargs= {**kwargs}, daemon=True)
    else:
        # We only allow one generation thread to run at a time
        return(the_thread)



def run_lyfe(window, **kwargs):
    """ Continually cycle through generations until a loop is detected.
    Args:
        window PySimpleGUI object: The handle of the window to place results on
        optional keyword arguments:
            update_freq: The number of generations between window updates.
    Returns:
        string: The status at the completion of all generations
    """
    n = 0
    seen = []
    debug_text = ""
    osc_cnt = 0
    osc_limit = 10   # default number of generations to keep going after a loop is detected
    update_freq = 1  # default number of generations between each window update.
    if 'update_freq' in kwargs:
        update_freq = kwargs['update_freq']

    global the_thread
    while the_thread != None:
        n += 1
        debug_text = f'Generation {n}'
        window['-DEBUG-'].update(debug_text)
        seen.insert(0, get_current_hash())
        do_a_single_generation()
        show_the_field(window)
        if get_current_hash() in seen:
            debug_text = f'Looped after {n-osc_cnt} generations'
            ago = seen.index(get_current_hash())
            if ago == 0:
                debug_text += f"\nFrozen"
            else:
                debug_text += f"\nLoop length is {ago+1}"
            window['-DEBUG-'].update(debug_text)
            osc_cnt += 1
            if osc_cnt > osc_limit:
                break

        if n % update_freq == 0:
            window.refresh()
        # This is a good place to put any small delay between generations
        # time.sleep(0.005)
    the_thread = None
    return(debug_text)



def start_lyfe_app(*args, **kwargs):
    # Create the application window. This is persistent until the application ends
    window = make_the_window()
    make_the_field()

    # Add twice as many cells as normal when we startup
    randomise_the_field(new_pct)
    randomise_the_field(new_pct)

    debug_text = "Conway's game of life\nNick's version anyway"

    # Process window events until the window is closed or the Quit button is pressed
    while True:

        #Display the field every time round
        show_the_field(window)

        # Update the debug area with relavent info (even if blank)
        window['-DEBUG-'].update(debug_text)

        # Wait for a button to be clicked (or other action)
        event, values = window.read()

        if event == 'Step':
            do_a_single_generation()
            debug_text = 'Stepping'
        elif event == 'Stop':
            stop_generation()
            debug_text = 'Stopping'
        elif event == 'Add cells':
            randomise_the_field(new_pct)
            debug_text = f'Adding {new_pct}% more cells'
        elif event == 'Clear':
            make_the_field()
            debug_text = f'Clearing the field'
        elif event == 'Load growth':
            load_pattern_1()
            debug_text = f'Loadding pattern 1'
        elif event == 'Up glider':
            load_pattern_up_glider()
            debug_text = f'Up glider'
        elif event == 'Down glider':
            load_pattern_2()
            debug_text = f'Loadding pattern 2'
        elif event == 'Left glider':
            load_pattern_left()
            debug_text = f'Loadding pattern 3'
        elif event == 'Interesting':
            load_pattern_4()
            debug_text = f'Loadding pattern 4'
        elif event == 'Massive glider':
            load_pattern_5()
            debug_text = f'Loadding pattern 5'
        elif event == 'Load 6':
            load_pattern_6()
            debug_text = f'Loadding pattern 6'
        elif event == '3 cycle':
            load_pattern_7()
            debug_text = f'Loadding pattern 7'
        elif event == 'Show neighbours':
            toggle_neighbours()
            debug_text = f'Neighbour count flipped'
        elif event == 'Show survivors':
            toggle_survivors()
            debug_text = f'Survivors count flipped'
        elif event == 'Run':
            debug_text = "Running?"
            global the_thread
            the_thread = run_lyfe_thread(window)
            if the_thread.is_alive() is False:
                the_thread.start()
        elif event == 'Quit' or event == sg.WIN_CLOSED:
            break
        else:
            debug_text = f"Event = {event}"


    kill_the_window(window)


if __name__ == "__main__":
    start_lyfe_app()

