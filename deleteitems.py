# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:11:25 2023

@author: Mark Larsen
"""
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from locators import Locators


class delPage():

    def __init__(self, driver, tabName, userCreds):
        self.driver = driver
        self.tabName = tabName
        self.delBadgeID_textbox_CSSSel = Locators.delBadgeID_textbox_CSSSel
        self.delPassword_textbox_CSSSel = Locators.delPassword_textbox_CSSSel
        self.delProblemSolve_menu_CSSSel = Locators.delProblemSolve_menu_CSSSel
        self.delDeleteItems_menu_CSSSel = Locators.delDeleteItems_menu_CSSSel
        self.delUrl = Locators.delUrl
        self.delDeleteContainer_textbox_CSSSel = \
            Locators.delDeleteContainer_textbox_CSSSel
        self.user_pass = userCreds.userPassword
        self.user_badgeid = userCreds.userBadgeID
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 30)

    def Open(self):

        # open Delete Items
        self.driver.execute_script(
            f"window.open('about:blank','{self.tabName}');")

        # It is switching to DeleteItems tab
        self.driver.switch_to.window(self.tabName)

        # navigate to the url
        self.driver.get(self.delUrl)

        # enter badge ID
        element = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.delBadgeID_textbox_CSSSel)))
        element.send_keys(self.user_badgeid)
        element.send_keys(Keys.ENTER)

        # enter user password
        element = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.delPassword_textbox_CSSSel)))
        element.send_keys(self.user_pass)
        element.send_keys(Keys.ENTER)

        element = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.delProblemSolve_menu_CSSSel)))

        # enter user Problem solve delete items app menu
        self.driver.get(
            'https://fcmenu-iad-regionalized.corp.amazon.com/DEN2/entry/220')

        if self.getCurrentDeletionMode() == "CONTAINER":
            self.changeDeleteMode()

    def getCurrentDeletionMode(self):
        # get the current mode
        self.vars["delete_mode"] = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, Locators.delDeletionMode_text_CSSSel)))
        return self.vars["delete_mode"]

    def changeDeleteMode(self):
        # Change the delete mode
        self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, Locators.delUserMenu_linktext_CSSSel))).click()
        if self.vars["delete_mode"] == "SINGLE":
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Locators.delContainerMode_radio_CSSSel))).click()
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Locators.delEnter_button_CSSSel))).click()
        else:
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Locators.delSingleMode_radio_CSSSel))).click()
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Locators.delEnter_button_CSSSel))).click()

    def check_exists(self, CSSSelector, containerId):
        # check if a given html object exists.
        try:
            wait = WebDriverWait(self.driver, 3)
            element = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, CSSSelector)))

            if containerId not in element.text:
                print(f'NOT found {CSSSelector} in browser')
                return False
            else:
                print(f'found {CSSSelector} in browser')
                return True
        except NoSuchElementException:
            print(f'{CSSSelector} does not exist')
            return False
        except TimeoutException:
            print(f"time out waiting for {CSSSelector}")
            return False

    def deleteItems(self):
        try:

            # get the number of items to delete
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 Locators.delEnter_button_CSSSel)))

            # wait for items to load
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 Locators.delItemList_radio_xpath)))

            items = self.driver.find_elements(
                By.XPATH, Locators.delItemList_radio_xpath)
            numItems = len(items) + 1
            print(f"found {numItems} items to delete")
            for i in range(1, numItems):
                print(i)
                # display item progress in header
                c = f"<span style=font-size:15px;color:red;>Processing {i} of {numItems -1}</span>"

                element = self.driver.find_element(By.CSS_SELECTOR,
                                                   Locators.delHeaderMessage_text_CSSSelector)
                if element:
                    self.driver.execute_script(
                        f"var ele=arguments[0]; ele.innerHTML = '{c}';", element)
                    print(
                        print(f"element found for header message {i} of {numItems}"))
                else:
                    print(
                        f"No element found for header message {i} of {numItems}")

                if i < numItems + 1:
                    # if there are items remaining then
                    # wait for items to load
                    self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         Locators.delItemList_radio_xpath)))

                self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                        Locators.delEnter_button_CSSSel))).click()
                print("found Select item to delete")

                # select the 'Damaged and unreturnable' option
                self.wait.until(EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, Locators.delHeaderMessage_text_CSSSel),
                    "Select deletion reason"))
                print("found selected deletion reason")

                self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                        Locators.delDamagedAndUnreturnable_radio_CSSSel))).click()
                print("click to damaged or unreturnable")

                # click the Continue button
                self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, Locators.delEnter_button_CSSSel))).click()
                print("selected damaged and unreturnable")

                # click the confirm deletion button
                self.wait.until(EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, Locators.delHeaderMessage_text_CSSSel),
                    "Confirm the deletion"))
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, Locators.delConfirmDeletion_button_xpath))).click()
                print("confirm deletion")

        except TimeoutException:
            try:
                # wait for the response from the container id search
                # check to see if the container is empty
                element = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, Locators.delAlertMsg_text_CSSSel)))
                if element.text == "Container confirmed is empty.":
                    print("Container confirmed is empty.")
                    return
            except TimeoutException:
                print("Container not empty")
                return

    def searchContainer(self, containerId):
        try:
            self.driver.switch_to.window(self.tabName)
            print("del search")

            # Find the search field and enter the container id into it
            # and press enter.
            element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.delDeleteContainer_textbox_CSSSel)))
            print(f"entering Container ID: {containerId}")
            element.send_keys(containerId)
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Locators.delEnter_button_CSSSel))).click()

            # Check to see if we got a valid response or a
            # service timeout error look for an alert message or
            # a service timeout error or
            # a radio button showing items available to delete
            css_search_elements = f"{Locators.delAlertMsg_text_CSSSel}, \
                {Locators.delServiceFail_text_CSSSel}, \
                    {Locators.delItemList_radio_CSSSel}"
            element = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_search_elements)))

            print(F"Element text found: {element.text}")
            print(f"class name: {element.get_attribute('class')}")
            if element.text == f"Container {containerId} is empty.":
                print(f"Container {containerId} is empty.")
                return containerId
            elif element.text == f"Input {containerId} is not a valid container.":
                print(f"Input {containerId} is not a valid container.")
                return containerId
            elif element.text == "The service failed to process your request":
                time.sleep(2)
                self.searchContainer(containerId)
            elif element.get_attribute("class") == "a-icon a-icon-radio":
                # Container is not empty delete the items from the container
                print("-> deleteItems")
                # time.sleep(2)
                self.deleteItems()
                return containerId

        except Exception as e:
            print(f"Exception: {str(e)}")
