# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:09:28 2023

@author: Mark Larsen
"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from locators import Locators
from bs4 import BeautifulSoup
import time


class panDashPage():

    def __init__(self, driver, tabName):
        self.driver = driver
        self.tabName = tabName
        self.url = Locators.url
        self.location_button_xpath = Locators.location_button_xpath
        self.sourcefilter_dropdown_id = Locators.sourcefilter_dropdown_id
        self.sourceFilter_option_text = Locators.sourceFilter_option_text
        self.siteid_textbox_xpath = Locators.siteid_textbox_xpath
        self.siteid_value_text = Locators.siteid_value_text
        self.asinsFilter_textbox_id = Locators.asinsFilter_textbox_id
        self.search_button_id = Locators.search_button_id
        self.wait = WebDriverWait(self.driver, 30)
        self.donatable = False
        self.level = 'level0'
        self.htrc = 0.0
        self.hazmat_exception = str("")
        self.un_classification = str("")
        self.limited_quantity_guidance = str("")
        self.result_color = str("")

        self.bs = BeautifulSoup()

    def Open(self):

        self.driver.execute_script(
            f"window.open('about:blank','{self.tabName}');")
        # switch to PanDash tab now
        self.driver.switch_to.window(f"{self.tabName}")

        # In the second tab, it opens PanDash
        self.driver.get(self.url)

    def set_default_params(self):
        # Set default search params
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.location_button_xpath)))
        element.click()

        el = self.driver.find_element(By.ID, self.sourcefilter_dropdown_id)
        for option in el.find_elements(By.TAG_NAME, 'option'):
            if option.text == self.sourceFilter_option_text:
                option.click()
                break

        # Enter Site ID as the FCInput
        element = wait.until(EC.presence_of_element_located(
            (By.XPATH, self.siteid_textbox_xpath)))
        element.send_keys(self.siteid_value_text)
        element.send_keys(Keys.TAB)

    def set_pandash_results(self, result):
        self.donatable = result[0]
        self.hrtc = result[1]
        self.hazmat_exception = result[2]
        self.un_classification = result[3]
        self.limited_quantity_guidance = result[4]

    def get_pandash_results(self):
        return [self.donatable, self.htrc, self.hazmat_exception,
                self.un_classification, self.limited_quantity_guidance]

    def is_donatable(self):
        return self.donatable

    def setResultMessage(self):

        css_search_elements = "'#resultMessage'"
        element = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#resultMessage')))

        if element is not None:
            c = ""
            self.driver.execute_script(
                f"var ele=arguments[0]; ele.innerHTML = '{c}';", element)
            print(f"Pandash result Message: {c}")

    def search(self, ASIN):
        self.driver.switch_to.window(f"{self.tabName}")
        element = self.driver.find_element(By.ID, self.asinsFilter_textbox_id)
        element.clear()
        element.send_keys(ASIN)
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(EC.element_to_be_clickable(
            (By.ID, self.search_button_id)))
        element.click()
        return self.parsePage(ASIN)

    def parsePage(self, ASIN):

        self.level = 'level0'
        self.results = []
        css_search_elements = "#resultMessage,#errorMessage"
        element = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_search_elements)))
        result = element.text
        print(result)

        if result == '0 result found.':
            print(f'result: {result}')
            return
        else:
            print(f'result: {result}')

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        grd = soup.find("table", class_="ui-jqgrid-btable")

        for idx, row in enumerate(grd.findAll("tr")):
            if idx == 0:
                continue

            cells = row.findAll("td")

            if len(cells) == 15:

                self.level = cells[1].get('data-color')
                asin = cells[2].get_text(strip=True)
                self.htrc = float(cells[6].get_text(strip=True) or 0)
                self.hazmat_exception = cells[7].get_text(strip=True)
                self.un_classification = cells[9].get_text(strip=True)
                self.limited_quantity_guidance = cells[10].get_text(strip=True)

                # Check pandash output for hazardous information and donation eligibility
                approved_hazmat_levels = [
                    'level1', 'level2', 'level4', 'level5']
                approved_classes = [2.1, 2.2, 3, 4, 8, 9]

                # is the item level and class of the item in the
                # approved lists?
                if self.level in approved_hazmat_levels and self.htrc in\
                        approved_classes:

                    # does the item have a UN number and exception message
                    # information?
                    if self.un_classification[:2] == 'UN' and \
                            len(self.hazmat_exception) > 0 and \
                            len(self.limited_quantity_guidance) > 0:
                        self.donatable = True

                    return self.level

                else:
                    if self.level == 'level1' and self.htrc == 0:
                        self.donatable = True
                    return self.level
