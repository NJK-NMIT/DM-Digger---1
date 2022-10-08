#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -q
# :(){ :|:& };: #ELaFB

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
  by the Medical Officer of Health who have a need to analyse information
  in the national register but lack the necessary skills in Microsoft Excel
  to do so.

Application purpose:
  The DM Digger application was created to make sense of the information in
  the published spreadsheet. It allows the user to interrogate the data to see
  which licensing authorities are processing the most applications and what part
  of the year has the most applications made. This allows the user to schedule
  their resources to the right part of the country at the right time of year.

"""

import pandas as pd
import PySimpleGUI as sg
import os.path
import sys

from model.Model_dm import Model_dm
import view.View_dm
import controller.Controller_dm
import controller.freq_analysis
import controller.appl_analysis
import controller.anom_analysis

sys.dont_write_bytecode = True


if __name__ == "__main__":

    # Initialise the DM enviroment
    dm = Model_dm()

    # Is everything ready to go?
    debug_text = dm.run_startup_checks()
    if debug_text != "":
        print(debug_text)

    # Get a login name
    login = ""
    while not login:
        login = view.View_dm.get_login(dm)
    # If the login window was closed then quit the whole application
    # Sidenote: You can't have a login name of "Quit" - The actual logins are
    #     always lowercase anyway.
    if login == 'Quit':
        quit()

    # Create the application window. This is persistent until the application ends
    # Reminder: Making the window elements also sets each element controller
    window = view.View_dm.make_the_window(dm)

    # Set the "info" element to the name of the (already) logged in user
    view.View_dm.info_update(window, f"Logged in as:\n  {login}")

    # handoff control to the window event processor.
    controller.Controller_dm.process_events(window, dm)

    # Cleanup.  Be a tidy Kiwi
    view.View_dm.kill_the_window(window)

