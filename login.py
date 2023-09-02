# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:09:06 2023

@author: markllar (markllar@amazon.com)
"""

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators import Locators

class LoginPage():
    
    def __init__(self, driver):
        self.driver = driver
        
        self.username_textbox_xpath = Locators.username_textbox_xpath
        self.username_button_xpath = Locators.username_button_xpath
        self.password_textbox_xpath = Locators.password_textbox_xpath
        self.password_button_xpath = Locators.password_button_xpath
        self.pincode_textbox_xpath = Locators.pincode_textbox_xpath
        self.pincode_button_xpath = Locators.pincode_button_xpath
        self.amazonlogin_button_xpath = Locators.amazonlogin_button_xpath
         
                   
    def get_amazon_login(self):
        # #Click on Amazon Login
        #load AUSTIN
        self.driver.get(Locators.austin_login_url)
                
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(EC.element_to_be_clickable((By.XPATH,self.amazonlogin_button_xpath)))
        element.click()
      
        
    def enter_username(self,username):
        #enter user name
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH,self.username_textbox_xpath)))
        element.send_keys(username)
        
        #Click the Sign in button
        element = wait.until(EC.element_to_be_clickable((By.XPATH, self.username_button_xpath)))
        element.click()

    def enter_pincode(self, pincode):
        #Enter Pin Code
        wait = WebDriverWait(self.driver, 30)
        element = wait.until(EC.element_to_be_clickable((By.XPATH,self.pincode_textbox_xpath)))
        element.send_keys(pincode)

        #Click the Submit button
        element = wait.until(EC.element_to_be_clickable((By.XPATH,self.pincode_button_xpath)))
        element.click()