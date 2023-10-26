# -*- coding: utf-8 -*-
"""
VSCode Editor

Author: Mark Larsen 

Help speed up donation processing


"""


from re import T
import time

# from selenium.webdriver.support.expected_conditions import element_attribute_to_include
from sql import db
import signal
from cfg_log import cfg
from webEvents import EventListener
from deleteitems import delPage
from fcr import FCRPage
from austin import AUSTINPage
from csi import CSIPage
from pandash import panDashPage
from denali import denaliPage
from login import LoginPage
from selenium.webdriver.support.event_firing_webdriver import \
    EventFiringWebDriver
from selenium import webdriver
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".", "."))
print(sys.path)


# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

wasteprocessing = False


class LoginDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.siteid = userCreds.getUserSiteID()
        self.after(250, lambda: self.title('Login'))
        self.result = False
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.getLocationSiteID()
        self.create_widgets()
        # <-- adding the protocol
        self.protocol("WM_DELETE_WINDOW", self.closed)

    def closed(self):
        print("login window closed")
        self.result = False
        self.destroy()

    def getLocationSiteID(self):
        if self.siteid == "SiteID":
            dialog = ctk.CTkInputDialog(
                text="Enter your site ID:", title="Site ID")
            dlgSiteID = dialog.get_input()
            print("Site ID:", dlgSiteID)
            userCreds.saveSiteID(dlgSiteID)

    def siteLogin(self):
        # donations login page
        # save the credentials
        self.result = userCreds.saveUser(self.user_entry.get(),
                                         self.user_pass.get(),
                                         self.user_badge.get(),
                                         self.user_pin.get(),
                                         self.checkbox.get())
        self.destroy()

    def create_widgets(self):
        # create the widgets for the login dialog

        self.frame = ctk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, pady=10, padx=10)

        self.label = ctk.CTkLabel(
            master=self.frame, text="Please enter your login credentials")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.badge_label = ctk.CTkLabel(
            master=self.frame, text="Badge ID:")
        self.badge_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.user_badge = ctk.CTkEntry(
            master=self.frame,  show="*")
        self.user_badge.grid(row=1, column=1, pady=10, padx=10)
        self.user_badge.insert(0, f'{userCreds.getUserBadgeID()}')

        self.user_label = ctk.CTkLabel(
            master=self.frame, text="User name:")
        self.user_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.user_entry = ctk.CTkEntry(
            master=self.frame)
        self.user_entry.grid(row=2, column=1, pady=10, padx=10)
        self.user_entry.insert(0, f'{userCreds.getUserName()}')

        self.pass_label = ctk.CTkLabel(
            master=self.frame, text="Password:")
        self.pass_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.user_pass = ctk.CTkEntry(
            master=self.frame, show="*")
        self.user_pass.grid(row=3, column=1, pady=12, padx=10)
        self.user_pass.insert(0, f'{userCreds.getUserPassword()}')

        self.pin_label = ctk.CTkLabel(
            master=self.frame, text="Pin:")
        self.pin_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.user_pin = ctk.CTkEntry(
            master=self.frame, show="*")
        self.user_pin.grid(row=4, column=1, pady=10, padx=10)
        self.user_pin.insert(0, f'{userCreds.getUserPinCode()}')

        self.donation_button = ctk.CTkButton(
            master=self.frame, text='Donations', command=self.siteLogin)
        self.donation_button.grid(row=5, column=1, pady=10, padx=10)

        self.waste_button = ctk.CTkButton(
            master=self.frame, text='Waste', command=self.wasteLogin)
        self.waste_button.grid(row=5, column=0, pady=10, padx=10)

        self.checkbox = ctk.CTkCheckBox(master=self.frame, text='Remember Me')
        self.checkbox.grid(row=6, column=1, pady=12, padx=10)

        self.donation_button.bind('<Return>', self.siteLogin)
        if userCreds.getUserRememberMe():
            self.checkbox.select()

    def wasteLogin(self):
        # log in to the appropriate sites for waste processing
        global wasteprocessing
        wasteprocessing = True
        self.siteLogin()


class MainWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.scanCode = ctk.StringVar()
        self.bind('<FocusIn>', set_focus)
        self.create_widgets()
        self.pack()
        self.bind('<Return>', self.findItem)
        self.login()

    def login(self):
        login_dialog = LoginDialog(self)
        win.wait_window(login_dialog)

        print(f"login result: {login_dialog.result}")

        if login_dialog.result:
            # login to the web sites
            print('login result: ', login_dialog.result)

            # initialize the web driver and classes
            self.driver = webdriver.Firefox()
            self.austinEventListener = EventListener()
            self.edriver = EventFiringWebDriver(
                self.driver, self.austinEventListener)
            self.austinLogin = LoginPage(self.edriver)
            self.panDash = panDashPage(self.edriver, 'pandash')
            self.denali = denaliPage(self.edriver, 'denali')
            self.csiRecall = CSIPage(self.edriver, 'recall')
            self.csiReject = CSIPage(self.edriver, 'website_reject')
            self.fcr = FCRPage(self.edriver, 'fcr', userCreds)
            self.delContainer = delPage(
                self.edriver, 'delContainer', userCreds)
            self.austin = AUSTINPage(self.edriver)

            self.austinLogin.get_amazon_login()
            self.austinLogin.enter_username(userCreds.getUserName())
            self.austinLogin.enter_pincode(userCreds.getUserPinCode())

            time.sleep(5)

            # Open PanDash
            self.panDash.Open()
            self.panDash.set_default_params()
            if not wasteprocessing:
                # Open Denali
                self.denali.Open()

                # Open CSI Recall
                self.csiRecall.Open()

                # Open CSI Website_reject
                self.csiReject.Open()

                # initialize Delete Items App
                self.delContainer.Open()

            # Initialize AUSTIN
            self.austin.Open()
            self.austin.setWasteProcessFlag(wasteprocessing)

            # initialize FC Research
            self.fcr.Open()

            self.austin.Open()
        else:
            print("login window was closed with out entry")
            self.destroy()
            return False

    def addBannedASIN(self):
        dialog = ctk.CTkInputDialog(
            text="Enter the banned ASIN:", title="Banned ASIN",)
        dlgBannedASIN = dialog.get_input()
        print("Banned ASIN:", dlgBannedASIN)
        r = sql_db.addBanned(dlgBannedASIN)

    def findItem(self, scan='', ASIN=None):

        self.pandash_result = []
        self.denali_result = str()
        self.csi_recall_result = str()
        self.csi_reject_result = str()
        self.barcode = scan
        self.container_result = str()
        self.cached_scan = False

        if not ASIN:
            self.ASIN = mw.scanCode.get().strip()
            mw.scanCode.delete(0, ctk.END)
            self.barcode = self.ASIN
        else:
            self.ASIN = ASIN
        print(f'Find item: {self.ASIN}')

        self.austin.resetStatusIndicator()

        if self.ASIN == 'config':
            # Open the config ini file
            userCreds.openConfig()
            return
        elif self.ASIN == 'banned':
            # add the banned ASIN to the banned ASINs list
            self.addBannedASIN()
            return
        elif self.ASIN[:3] == 'tsX' or self.ASIN[:6] == 'tscage':
            # Switch to the delete items page and delete items from
            # the container
            self.delContainer.searchContainer(self.ASIN)
            return True

        # check for previously cached scans
        result = sql_db.get_scan(self.ASIN)
        if result:
            self.cached_scan = True
            self.panDash.set_pandash_results(result[-5:])
            self.ASIN = self.austin.searchASIN(self.ASIN)
            self.austin.setStatusColor('Cache', result[3:7])
            self.austin.setStatusIndicator(
                self.panDash.get_pandash_results(), self.cached_scan)
            return True

        elif self.ASIN[:3] == 'X00':
            self.ASIN = self.austin.searchASIN(self.ASIN)
            self.pandash_result = self.panDash.search(self.ASIN)
            self.austin.setStatusColor('panDash', self.pandash_result)
            self.austin.setStatusIndicator(
                self.panDash.get_pandash_results())
            return True

        # search for the ASIN
        self.ASIN = self.austin.searchASIN(self.ASIN)

        if self.ASIN[:3] in ['LPN', 'FBA']:
            self.ASIN = self.fcr.searchASIN(self.ASIN)
            if self.ASIN is not None:
                self.findItem(self.barcode, self.ASIN)
            return True

        elif self.ASIN[:2] == 'B0' or len(self.ASIN) == 10:
            self.ASIN = self.austin.searchASIN(self.ASIN)

            if sql_db.isBanned(self.ASIN):
                self.austin.setBannedStatus()
                return
            else:
                self.pandash_result = self.panDash.search(self.ASIN)
                self.panDash_result_color = self.austin.setStatusColor(
                    'panDash', self.pandash_result)
                self.austin.setStatusIndicator(
                    self.panDash.get_pandash_results())

                # if the pandash result is level0 then return as it cannot
                # be donated
                if self.pandash_result == 'level0':
                    return

                # if user is processing donations
                if wasteprocessing is False:
                    print("look up in denali")
                    self.denali_result = self.denali.search(self.ASIN)
                    if self.denali_result and self.panDash.is_donatable():
                        # Amazon item is eligible for donation
                        print(f"denali_result: {self.denali_result}")
                        self.austin.setStatusColor(
                            'denali', self.denali_result)
                        self.austin.setStatusIndicator(
                            self.panDash.get_pandash_results())
                        print(self.panDash.get_pandash_results())

                        print("look up in CSIs")
                        self.csi_recall_result = self.csiRecall.searchASIN(
                            self.ASIN)
                        # update display
                        self.austin.setStatusColor(
                            'csiRecall', self.csi_recall_result)
                        if self.csi_recall_result:
                            self.csi_reject_result = self.csiReject.searchASIN(
                                self.ASIN)
                            # update display
                            self.austin.setStatusColor(
                                'csiReject', self.csi_reject_result)
                            self.austin.Open()
                    else:
                        # FBA item is not eligible for donation
                        print(f"denali_result: {self.denali_result}")
                        self.austin.setStatusColor(
                            'denali', self.denali_result)
                        self.austin.setStatusIndicator(
                            self.panDash.get_pandash_results())

                self.austin.setStatusIndicator(
                    self.panDash.get_pandash_results())
                # add the scan to the cache table if not already there

        if not self.cached_scan:
            result_colors = self.austin.get_status_colors()
            pd_results = self.panDash.get_pandash_results()
            print(result_colors, pd_results)
            # pd_results.insert(0, result_colors[0])

            sql_db.add_scan(self.barcode, self.ASIN,
                            result_colors[0],
                            result_colors[1],
                            result_colors[2],
                            result_colors[3],
                            pd_results[0],
                            pd_results[1],
                            pd_results[2],
                            pd_results[3],
                            pd_results[4])

        # # if the user enters config in the barcode scan dialog open the ini file
        # if self.ASIN == 'config':
        #     mw.scanCode.delete(0, ctk.END)
        #     userCreds.openConfig()
        #     return

        # if self.ASIN == 'banned':
        #     mw.scanCode.delete(0, ctk.END)
        #     self.addBannedASIN()
        #     return

        # print(f'Find item: {self.ASIN}')
        # mw.scanCode.delete(0, ctk.END)

        # if self.ASIN[:3] == 'tsX' or self.ASIN[:6] == 'tscage':
        #     print(f'container {self.ASIN}')
        #     # this is a container
        #     # switch to container mode
        #     # self.austin.set_scan_type("Tote")
        #     # self.container_result = self.austin.search_container(self.ASIN)
        #     # if self.container_result == "empty_container":
        #     self.delContainer.searchContainer(self.ASIN)
        #     # self.austin.set_scan_type("Product")
        #     return

        # else:
        #     # check for previously cached scans
        #     result = sql_db.get_scan(self.ASIN)
        #     if result:
        #         self.cached_scan = True
        #         self.panDash.set_pandash_results(result[-5:])
        #         self.austin.setStatusColor('Cache', result[3:7])
        #         self.austin.setStatusIndicator(
        #             self.panDash.get_pandash_results(), self.cached_scan)
        #         self.ASIN = self.austin.searchASIN(self.ASIN)
        #         return True
        #     elif self.ASIN[:3] == 'X00':
        #         self.ASIN = self.austin.searchASIN(self.ASIN)
        #         print(f"look up FBA in pandash {self.ASIN}")
        #         self.pandash_result = self.panDash.search(self.ASIN)
        #         self.austin.setStatusColor('panDash', self.pandash_result)
        #         self.austin.setStatusIndicator(
        #             self.panDash.get_pandash_results())
        #         return
        #     else:
        #         self.ASIN = self.austin.searchASIN(self.ASIN)

        # if self.ASIN[:3] == 'LPN' or self.ASIN[:3] == 'FBA':
        #     print("fcr find ASIN")
        #     self.ASIN = self.fcr.searchASIN(self.ASIN)

        #     # if we find and ASIN in FC Research then search the ASIN.
        #     if self.ASIN is not None:
        #         print(f"ASIN returned from fcr {self.ASIN}")

        #         # clear the search box and enter the ASIN
        #         # that was found and search
        #         mw.scanCode.delete(0, ctk.END)
        #         mw.scanCode.insert(0, self.ASIN)
        #         self.findItem(self.ASIN)
        # else:

        #     if sql_db.isBanned(self.ASIN):
        #         self.austin.setBannedStatus()
        #         return
        #     elif self.ASIN[:2] == 'B0' or len(self.ASIN) == 10:
        #         # # check for previously cached scans
        #         # result = sql_db.get_scan(self.ASIN)
        #         # if result:
        #         #     self.cached_scan = True
        #         #     self.panDash.set_pandash_results(result[-5:])
        #         #     self.austin.setStatusColor('Cache', result[3:7])
        #         #     self.austin.setStatusIndicator(
        #         #         self.panDash.get_pandash_results(), self.cached_scan)
        #         # else:
        #         print("look up in pandash")
        #         self.pandash_result = self.panDash.search(self.ASIN)
        #         self.panDash_result_color = self.austin.setStatusColor(
        #             'panDash', self.pandash_result)
        #         self.austin.setStatusIndicator(
        #             self.panDash.get_pandash_results())
        #         if self.pandash_result == 'level0':
        #             return

        #         if wasteprocessing is False:
        #             print("look up in denali")
        #             self.denali_result = self.denali.search(self.ASIN)
        #             if self.denali_result and self.panDash.is_donatable():
        #                 # Amazon item is eligible for donation
        #                 print(f"denali_result: {self.denali_result}")
        #                 self.austin.setStatusColor(
        #                     'denali', self.denali_result)
        #                 self.austin.setStatusIndicator(
        #                     self.panDash.get_pandash_results())
        #                 print(self.panDash.get_pandash_results())

        #                 print("look up in CSIs")
        #                 self.csi_recall_result = self.csiRecall.searchASIN(
        #                     self.ASIN)
        #                 # update display
        #                 self.austin.setStatusColor(
        #                     'csiRecall', self.csi_recall_result)
        #                 if self.csi_recall_result:
        #                     self.csi_reject_result = self.csiReject.searchASIN(
        #                         self.ASIN)
        #                     # update display
        #                     self.austin.setStatusColor(
        #                         'csiReject', self.csi_reject_result)
        #                     self.austin.Open()
        #             else:
        #                 # FBA item is not eligible for donation
        #                 print(f"denali_result: {self.denali_result}")
        #                 self.austin.setStatusColor(
        #                     'denali', self.denali_result)
        #                 self.austin.setStatusIndicator(
        #                     self.panDash.get_pandash_results())

        #         self.austin.setStatusIndicator(
        #             self.panDash.get_pandash_results())
        #         # add the scan to the cache table if not already there
        #         if not self.cached_scan:
        #             result_colors = self.austin.get_status_colors()
        #             pd_results = self.panDash.get_pandash_results()
        #             print(result_colors, pd_results)
        #             # pd_results.insert(0, result_colors[0])

        #             sql_db.add_scan(self.barcode, self.ASIN,
        #                             result_colors[0],
        #                             result_colors[1],
        #                             result_colors[2],
        #                             result_colors[3],
        #                             pd_results[0],
        #                             pd_results[1],
        #                             pd_results[2],
        #                             pd_results[3],
        #                             pd_results[4])

    def create_widgets(self):
        self.scanCode = ctk.CTkEntry(
            self, placeholder_text="Scan Barcode", width=250)
        self.scanCode.grid(row=0, column=0, padx=5, pady=5)
        self.findButton = ctk.CTkButton(
            self, text="Find", command=self.findItem)
        self.findButton.grid(row=0, column=2, padx=5, pady=5)
        self.findButton.bind('<Return>', self.findItem)
        self.scanCode.bind('<Control-v>', self.paste)
        self.scanCode.after(10, self.scanCode.focus_set())

    def paste(self, event=None):
        self.scanCode.event_generate("<<Paste>>")


def set_focus(*args):
    """triggers when the window gains focus."""
    mw.scanCode.focus_set()


def center_window(dlg, width=300, height=200):
    # get screen width and height
    screen_width = dlg.winfo_screenwidth()
    screen_height = dlg.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    dlg.geometry('%dx%d+%d+%d' % (width, height, x, y))

  # Function to be called when the timer expires


def myFunction():
    # return the scan box to standard color
    mw.scanCode.configure(fg_color='#343638')

# Function with the timer


def myTimer(seconds):
    time.sleep(seconds)
    myFunction()


def on_closing():
    print('shutting down')

    userCreds.saveAppInfo(str(win.winfo_x()), str(win.winfo_y()), str(1))
    msg = CTkMessagebox(title="Exit?", message="Do you want to quit?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()

    if response == "Yes":
        # del banned
        mw.driver.quit()
        win.quit()
        win.destroy()


if __name__ == '__main__':

    # load the user credentials from the ini file
    userCreds = cfg()
    sql_db = db()

    win = ctk.CTk()
    win.maxsize(450, 40)
    win.geometry(f"450x40+{userCreds.getWinXpos()}+{userCreds.getWinYpos()}")
    win.attributes('-topmost', True)
    win.title("Processing Assistant")

    mw = MainWindow(win)
    win.bind('<Return>', mw.findItem)

    signal.signal(signal.SIGTERM, on_closing)
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()
