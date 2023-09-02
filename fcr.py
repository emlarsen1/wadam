# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 03:24:29 2023

@author: Mark Larsen
"""
from CTkMessagebox import CTkMessagebox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators import Locators
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# import pandas as pd
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
import time


class FCRPage():

    def __init__(self, driver, tabName, userCreds):
        self.driver = driver
        self.tabName = tabName
        self.userbadge_textbox_xpath = Locators.userbadge_textbox_xpath
        self.userpass_textbox_xpath = Locators.userpass_textbox_xpath
        self.fcr_FCResearch_button_xpath = Locators.fcr_FCResearch_button_xpath
        self.fcr_problem_solve_button_xpath = \
            Locators.fcr_problem_solve_button_xpath
        self.fcrLoginUrl = Locators.fcrLoginUrl
        self.user_pass = userCreds.userPassword
        self.user_badgeid = userCreds.userBadgeID
        self.fcr_app_menu_text_CSSSel = Locators.fcr_app_menu_text_CSSSel

        # self.csiSearchURL = Locators.csiSearchURL

    def Open(self):

        # open FC Research
        self.driver.execute_script(
            f"window.open('about:blank','{self.tabName}');")

        # It is switching to FCR tab
        self.driver.switch_to.window(self.tabName)

        # navigate to the url
        self.driver.get(self.fcrLoginUrl)

        # enter badge ID
        wait = WebDriverWait(self.driver, 15)
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.userbadge_textbox_xpath)))
        element.send_keys(self.user_badgeid)
        element.send_keys(Keys.ENTER)

        # enter user password
        wait = WebDriverWait(self.driver, 15)
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.userpass_textbox_xpath)))
        element.send_keys(self.user_pass)
        element.send_keys(Keys.ENTER)

        msg = CTkMessagebox(
            title="FC Research", message="Please answer survey questions \
                manually then press Ok", icon="warning",
            option_1="Ok", option_focus=1)
        response = msg.get()

        if response == "Ok":

            wait = WebDriverWait(self.driver, 30)
            element = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.fcr_app_menu_text_CSSSel)))

            # FC Research Menu shortcut key= 308
            self.driver.get(
                'https://fcmenu-iad-regionalized.corp.amazon.com/DEN2/entry/308\
                    ')

    def getASIN(self, LPN):
        # check the inventory history table any history of the LPN and return
        # the corresponding
        # ASIN if available.
        try:
            if LPN[:3] == 'LPN':
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                            Locators.fcr_LPNTable_ASIN_text_CSSSel)))
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                grd = soup.find(
                    'table', attrs={"aria-describedby":
                                    "table-inventory-history_info"})

                for idx, row in enumerate(grd.findAll("tr")):
                    if idx == 0:
                        continue
                    cells = row.findAll("td")

                    if len(cells) == 14:
                        ASIN = cells[3].get_text(strip=True)
                        LPNnew = cells[6].get_text(strip=True)
                        if LPN != LPNnew:
                            print('existing LPN data present')

                        else:
                            print(f'search returned: {ASIN}')
                            return ASIN
                    else:
                        return
            elif LPN[:3] == 'FBA':
                # if this is an FBA code then look for the asin in the
                # table-sscc-info table
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                            Locators.fcr_FBATable_ASIN_text_CSSSel
                         ))).text.strip()
                if element is not None:
                    return element
                else:
                    return

        except TimeoutException:
            print('No ASIN Found')
            return

    def searchASIN(self, LPN):

        # search the LPN number for any history. If not found on first shearch
        # extend the range to the maximum 180 days and search again.

        self.driver.switch_to.window(self.tabName)
        print("fcr search")
        # Find the search field and enter the ASIN into it and press enter.

        print(f"entering LPN: {LPN}")
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="search"]')))
        element.send_keys(LPN)
        element.send_keys(Keys.ENTER)
        time.sleep(2)

        result = self.getASIN(LPN)
        if result is not None:
            return result
        else:
            print('No ASIN Found')
            # Subtract 180 days from current date and set search params
            d = datetime.today() - timedelta(days=180)
            print("Set search start date")
            print(d.strftime("%m/%d/%Y"))

            wait = WebDriverWait(self.driver, 10)
            element = wait.until(
                EC.element_to_be_clickable((By.ID, 'searchStart')))
            element.click()
            element.clear()
            element.send_keys(d.strftime("%m/%d/%Y"))
            element.send_keys(Keys.TAB)

            # Click Search
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.a-button-text')))
            element.click()

            result = self.getASIN(LPN)
            return result
