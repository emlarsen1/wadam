# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:09:40 2023

@author: markllar
"""
from locators import Locators
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CSIPage():
    
    
    def __init__(self, driver, tabName):
        self.driver = driver
        self.tabName = tabName
        self.prohibitedWords = Locators.prohibitedWords      
        self.csiURL = Locators.csiURL 
        self.csiSearchURL = Locators.csiSearchURL
        

    def Open(self):
        
        #open CSI
        self.driver.execute_script(f"window.open('about:blank','{self.tabName}');")
                
        #It is switching to CSI tab
        self.driver.switch_to.window(self.tabName)
 
        #navigate to the url
        self.driver.get(self.csiURL)

    def searchASIN(self,ASIN):
        
        self.driver.switch_to.window(self.tabName)
        #url = self.csiSearchURL
        url = f"https://csi.amazon.com/view?view=blame_o&item_id={ASIN}&marketplace_id=1&customer_id=&merchant_id=&sku=&fn_sku=&gcid=&fulfillment_channel_code=&listing_type=purchasable&submission_id=&order_id=&external_id=&search_string={self.tabName}&realm=USAmazon&stage=prod&domain_id=&keyword=&submit=Show"
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#item_summary_div > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > fieldset:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > b:nth-child(1)")))        

        pageSource = self.driver.page_source
        soup = BeautifulSoup(pageSource,"html.parser")
        print('got csi soup')
        
        status = soup.find('span', class_='healthy')
        if status is not None:
            print('found healthy')
            return '#33CC02'
        else:
            print('healthy not found')
            status = soup.find('span', class_='unhealthy')
            if status is not None:
                print('found unhealthy')
                errors = soup.find('li',class_="errors")
                if errors is not None:
                    #look for prohibited words
                    print(f"checking for prohibited words")
                    #prohibitedWords = ['recalled', 'prohibited', 'yanked', 'restricted', 'recall', 'reject', 'rejected', 'shadow']
                    print(self.prohibitedWords)
                    if any(word in errors.get_text().lower() for word in self.prohibitedWords):
                        print(errors.get_text().lower())
                        print('NOT eligible for donation')
                        return 'red'
                    else:
                        print('no restrictions')
                        return '#33CC02'
        
        
        