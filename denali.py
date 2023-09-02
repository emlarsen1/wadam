""" 
This module implements ASIN lookups in Denali 
to determine item eligibility for donation

 """


# import pytest
import time
# import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from locators import Locators
from bs4 import BeautifulSoup
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class denaliPage():
    def __init__(self, driver, tabName):
        self.driver = driver
        self.tabName = tabName
        self.denaliUrl = Locators.denaliUrl
        self.denaliEntry_Text_XPATH = Locators.denaliEntry_Text_XPATH
        self.denaliSubmit_button_CSSSel = Locators.denaliSubmit_button_CSSSel

    def teardown_method(self, method):
        self.driver.quit()

    def Open(self):
        # open Denali
        self.driver.execute_script(
            f"window.open('about:blank','{self.tabName}');")

        # It is switching to DeleteItems tab
        self.driver.switch_to.window(self.tabName)

        # navigate to the url
        self.driver.get(self.denaliUrl)

    def search(self, ASIN):
        # set up variables
        DEN2 = str()
        located = False
        iog_retail = False
        iog_warehouse = False
        iog_other = False

        self.driver.switch_to.window(f"{self.tabName}")

        try:
            # Select the ASIN field
            element = self.driver.find_element(
                By.CLASS_NAME, 'form-control')
            if element:
                element.clear()
                element.send_keys(ASIN)

            # Click the Submit button
            element = self.driver.find_element(
                By.CSS_SELECTOR, self.denaliSubmit_button_CSSSel)
            if element:
                element.click()

            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            denaliString = soup.find(
                "div", {"data-testid": "gpi-info-string-debug-tab__container"})

            gpi = str(denaliString).splitlines()
            for l in gpi:
                # print(l)
                if 'Dc = DEN2' in l:
                    located = True
                    print('located Dc = DEN2')
                    DEN2 = DEN2 + l.strip() + '\n'
                elif located:
                    if 'Dc = ' in l:
                        print('found next Dc = ')
                        located = False
                        break
                    else:

                        DEN2 = DEN2 + l.strip() + '\n'
                        # only inventory owener group 1 or 37
                        if 'Owner = ' in l:
                            iog = l.split()
                            iog = int(iog[2])
                            if iog == 1:
                                iog_retail = True
                                print(f'retail owner: {iog_retail}')
                            if iog == 37:
                                iog_warehouse = True
                                print(f'warehouse owner: {iog_warehouse}')
                            if iog != 1 and iog != 37:
                                iog_other = True
                                print(f'other owner: {iog_other}')
                            print(f'found owner: {iog}')

            print('*************************************')
            if (iog_retail or iog_warehouse) and not iog_other:
                print('Donatable')
                return True
            else:
                print('Not Donatable')
                return False
        except Exception as e:
            print(f'Denali Exception: {e}')
            return False
