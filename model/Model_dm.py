"""
This is where the Model_dm class is defined.

Data lives here.
Data goes here to die.
"""

import os.path



class Model_dm:


    # Create a dictionary of constants rather than scatter them through the source
    def __init__(self, data_source = None) -> None:
        self.in_url   = "https://www.justice.govt.nz/assets/Documents/Publications/May-2022-Certificates.xlsx"
        self.url_loc  = "https://www.justice.govt.nz/tribunals/arla/register-of-licences-and-certificates/"
        self.logo     = "DM Digger logo.png"
        self.Freq_img = "Frequency example.png"
        self.Appl_img = "Application example.png"
        self.Anom_img = "Anomaly example.png"

    # Methods to get at the constants
    def get_logo(self):
        return(self.logo)

    def get_freqimg(self):
        return(self.Freq_img)

    def get_applimg(self):
        return(self.Appl_img)

    def get_amonimg(self):
        return(self.Anom_img)


    def run_startup_checks(self):
        """
        Before the application main loop can start, we check that a set of
        preconitions are met.
        These are warnings rather than fatal errors.

        Returns:
            string: A list of failed checks.  An empty string if all checks are ok.

        """
        errors = []
        filename = self.get_logo()
        if os.path.exists(filename) != True:
            errors.append(f"Logo file '{filename}' not found")
            self.logo = ''
        filename = self.Freq_img
        if os.path.exists(filename) != True:
            errors.append(f"Frequency image file '{filename}' not found")
        filename = self.Appl_img
        if os.path.exists(filename) != True:
            errors.append(f"Application image file '{filename}' not found")
        filename = self.Anom_img
        if os.path.exists(filename) != True:
             errors.append(f"Anomaly image file '{filename}' not found")

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