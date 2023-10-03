# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:09:19 2023

@author: Mark Larsen
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from locators import Locators
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sql as scans


class AUSTINPage():

    def __init__(self, driver):
        self.driver = driver
        self.panDashColor = 'black'
        self.denaliColor = 'black'
        self.csiRecallColor = 'black'
        self.csiRejectColor = 'black'
        self.regulatedFlag = False
        self.category = str("")
        self.wasteprocessing = False
        self.asin_location_xpath = Locators.asin_location_xpath
        self.asin_regulated_xpath = Locators.asin_regulated_xpath
        self.asin_category_xpath = Locators.asin_category_xpath
        self.wait = WebDriverWait(self.driver, 30)

    def Open(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def check_exists_by_xpath(self, xpath):
        # check if a given html object exists.
        try:
            wait = WebDriverWait(self.driver, 3)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # self.driver.find_element(By.XPATH, xpath)
            print('path exists')
            return True
        except NoSuchElementException:
            print('path does not exist')
            return False
        except TimeoutException:
            print("time out waiting for element")
            return False

    def setWasteProcessFlag(self, flag):
        # set the flag as to what type of processing the user is doing
        # false = donations processing, true is waste processing.
        self.wasteprocessing = flag

    def setStatusColor(self, source, color):
        # colors are located here: https://pandash.amazon.com/styles/style.css

        hazColor = str()

        if source == 'panDash':

            print(f'the level returned is: {color}')

            # set the color of the hazardous level
            if color == 'level0':
                hazColor = '#999999'
            elif color == 'level1':
                hazColor = '#33CC02'
            elif color == 'level2':
                hazColor = '#FFE103'
            elif color == 'level3':
                hazColor = '#FFBF03'
            elif color == 'level4':
                hazColor = '#FF8002'
            elif color == 'level5':
                hazColor = '#FF4001'
            elif color == 'level6':
                hazColor = '#ED0700'
            elif color == 'level7':
                hazColor = '#AD03DE'
            elif color == 'level8':
                hazColor = '#3333FF'
            elif color == 'level9':
                hazColor = 'red'

            self.panDashColor = hazColor
            print(f'hazColor: {hazColor}')
        elif source == 'denali':
            if color:
                # Amazon item eligible for donation
                self.denaliColor = '#33CC02'
            else:
                # FBA item not eligible for donation
                self.denaliColor = 'red'

        elif source == 'csiRecall':
            self.csiRecallColor = color
        elif source == 'csiReject':
            self.csiRejectColor = color

    def setRegulatedFlag(self, flag):
        self.regulatedFlag = flag

    def resetStatusIndicator(self):

        # reset colors before each barcode search.
        self.panDashColor = 'black'
        self.denaliColor = 'black'
        self.csiRecallColor = 'black'
        self.csiRejectColor = 'black'
        self.regulatedFlag = False
        self.setStatusIndicator([False])

    def setStatusIndicator(self, pandash_results):
        # Show a simplified go no go for donations. 4 greens is donatable
        # if any other colors are displayed then further research is required to
        # determine if it is hazardous or not.

        self.driver.switch_to.window(self.driver.window_handles[0])

        if self.regulatedFlag == True:
            regResult = "<br><span style=font-size:35px;color:red;><sup>Regulated</sup></span>"
        else:
            regResult = ""

        c = f"<span style=font-size:150px;color:{self.panDashColor};>&#x2022;</span>\
            <span style=font-size:150px;color:{self.denaliColor};>&#x2022;</span>\
                <span style=font-size:150px;color:{self.csiRecallColor};>&#x2022;</span>\
                    <span style=font-size:150px;color:{self.csiRejectColor};>&#x2022;</span>\
                        {regResult}"

        # add hazardous donation information if donatable
        if pandash_results[0] and self.denaliColor == '#33CC02' \
                and pandash_results[1] > 0.0:
            c = c + \
                f"<span style=font-size:25px;color:blue;><br>Haz Donatable  \
                <br>HazClass: {pandash_results[1]}  <br>UN: {pandash_results[3]} \
                    <br>Exception: {pandash_results[2]}  <br>Guidance: {pandash_results[4]}"

        # check special categories
        if self.category == 'automotive':
            c = c + \
                f"<span style=font-size:20px;color:orange;><br>Caution \
                    Category: {self.category}  \
                        FBR does not want automotive items"
        elif self.category == 'drugstore':
            c = c + \
                f"<span style=font-size:20px;color:orange;><br>Caution \
                    Category: {self.category}  Check for OTC items"

        element = self.driver.find_element(
            By.CSS_SELECTOR, "h4.MuiTypography-root")
        self.driver.execute_script(
            f"var ele=arguments[0]; ele.innerHTML = '{c}';", element)

        element = self.driver.find_element(
            By.CSS_SELECTOR, "path.core-1r4552x-AustinLogo-austin:nth-child(12)")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        element = self.driver.find_element(By.CSS_SELECTOR, "#productId")
        element.click()

    def setBannedStatus(self):
        # if the item was previously rejected by C-Ops then reject it even if all other indicators
        # allow a donation.
        self.driver.switch_to.window(self.driver.window_handles[0])

        c = "<br><span style=font-size:35px;color:red;>C-Ops BANNED ITEM</span>"

        element = self.driver.find_element(
            By.CSS_SELECTOR, "h4.MuiTypography-root")
        self.driver.execute_script(
            f"var ele=arguments[0]; ele.innerHTML = '{c}';", element)

        element = self.driver.find_element(
            By.CSS_SELECTOR, "path.core-1r4552x-AustinLogo-austin:nth-child(12)")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        element = self.driver.find_element(By.CSS_SELECTOR, "#productId")
        element.click()

    def set_scan_type(self, scan_type: "Product"):
        element = self.driver.find_element(
            By.CSS_SELECTOR, f"input[value={scan_type}]").click()
        if element:
            return True
        else:
            return False

    def search_container(self, container_id):
        try:
            # TODO: add the container search function

            print("wait to see if we get a container with items")
            # Check if we get a container with items or and empty container
            css_search_elements = f"{Locators.container_found_CSSSel}, \
                {Locators.container_empty_CSSSel}"
            element = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_search_elements)))

            print(F"Element text found: {element.text}")
            # container found
            if element.text[:6] == "[Tote]":
                return str(container_id)
            # If the container is empty, then return.
            elif element.text[:19] == "This tote is empty.":
                return "empty_container"

        except NoSuchElementException:
            print("Container not found")
            return str(container_id)

    def setWasteContainerTab(self):
        # if the user is clicked on donations login then automatically select the tab for
        # the donations containers to add items to.
        if self.wasteprocessing == False:
            element = self.driver.find_element(
                By.CSS_SELECTOR, "button.MuiTab-root:nth-child(2)")
            if element is not None:
                element.click()

    def checkRegulatedStatus(self):
        try:
            print("wait to see if we get a Regulated Result")
            if self.check_exists_by_xpath(self.asin_regulated_xpath):
                element = self.driver.find_element(
                    By.XPATH, self.asin_regulated_xpath).text
                if element == "REGULATED":
                    self.setRegulatedFlag(True)
                    print("ASIN REGULATED")
                else:
                    self.setRegulatedFlag(False)
            else:
                self.setRegulatedFlag(False)
        except NoSuchElementException:
            self.setRegulatedFlag(False)

    def get_category(self):
        try:
            print("get the property category")

            if self.check_exists_by_xpath(self.asin_category_xpath):
                element = self.driver.find_element(
                    By.XPATH, self.asin_category_xpath).text.strip()
                self.category = element[3:]
        except NoSuchElementException:
            self.category = ''

    def searchASIN(self, ASIN):
        # Enter the scaned barcode into the search box and check if austin
        # is able to locate and ASIN for the item. if it is then return the ASIN
        self.driver.switch_to.window(self.driver.window_handles[0])
        print("find product ID input field")
        element = self.driver.find_element(By.CSS_SELECTOR, "#productId")
        element.send_keys(ASIN)
        element.send_keys(Keys.ENTER)

        try:
            print("wait to see if we get an ASIN")
            # Check if we get an ASIN or not recognized as an ASIN
            css_search_elements = f"{Locators.asin_location_CSSSel}, \
                {Locators.asin_not_found_CSSSel}"
            element = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_search_elements)))

            print(F"Element text found: {element.text}")
            # ASIN found
            if element.text[:5] == "ASIN:":
                element = element.text.split(":")
                ASIN = element[1].strip()
                print("ASIN Found")
                self.setWasteContainerTab()
                self.checkRegulatedStatus()
                self.get_category()
                return str(ASIN)
            # Not recognized as an ASIN
            elif element.text == "We don't recognize this item, it may not be \
                part of our inventory. Please scan again or contact our waste \
                    or donation vendors for more information.":
                return str(ASIN)

            else:
                return str(ASIN)

        except NoSuchElementException:
            print("ASIN not found")
            return str(ASIN)
