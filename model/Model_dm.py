"""
This is where the Model_dm class is defined.

Data lives here.
Data also goes here to die.
"""

import os.path
import pandas as pd



class Model_dm:


    def __init__(self, data_source = None) -> None:
        # Create a dictionary of constants rather than scatter them through the source
        self.in_url   = "https://www.justice.govt.nz/assets/Documents/Publications/May-2022-Certificates.xlsx"
        self.url_loc  = "https://www.justice.govt.nz/tribunals/arla/register-of-licences-and-certificates/"
        self.logo     = "images/DM Digger logo.png"

        # Create and store an empty frame
        self.frame = pd.DataFrame()

        # Keep track of what the last screen was
        self.state = None

        # Somewhere to keep the last aggregator
        self.fig_canvas_agg = None

        # Keep track of the last data update timestamp
        self.last_update = None

        # Once we're loggin in, keep track of who we are (and proof)
        self.login = None
        self.auth_key = None

    # Methods to get at the constants
    def get_logo(self):
        return(self.logo)

    def get_state(self):
        return(self.state)

    def get_login(self):
        return(self.login)

    def set_state(self, state):
        self.state = state

    def set_login(self, login):
        self.login = login


    def run_startup_checks(self):
        """
        Before the application main loop can start, we check that a set of
        preconitions are met.
        These are warnings rather than fatal errors.

        Note that these checks are not in the __init__ section on purpose,
        "Startup" checks could be run at any time, not just at initialisation.

        Returns:
            string: A list of failed checks.  An empty string if all checks are ok.

        """
        errors = []

        filename = self.get_logo()
        if os.path.exists(filename) != True:
            errors.append(f"Logo file '{filename}' not found")
            self.logo = ''

        return f"\n".join(errors)
    

    def is_excel_filetype(self, filename):
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


    def set_frequency_data(self, data):
        self.Freq_data = data


    def set_analysis_data(self, data):
        self.Anal_data = data


    def set_anomaly_data(self, data):
        self.Anom_data = data
