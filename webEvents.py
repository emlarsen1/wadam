# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 02:15:57 2023

@author: Mark Larsen
"""


from selenium.webdriver.support.events import AbstractEventListener


class EventListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        print("Before navigating to ", url)

    def after_navigate_to(self, url, driver):
        print("After navigating to ", url)

    def before_navigate_back(self, driver):
        print("before navigating back ", driver.current_url)

    def after_navigate_back(self, driver):
        print("After navigating back ", driver.current_url)

    def before_navigate_forward(self, driver):
        print("before navigating forward ", driver.current_url)

    def after_navigate_forward(self, driver):
        print("After navigating forward ", driver.current_url)

    def before_find(self, by, value, driver):
        print("before find: " + value)

    def after_find(self, by, value, driver):
        print("after_find element name:" + value)

    def before_click(self, element, driver):
        print("before_click")

    def after_click(self, element, driver):
        print("after_click")

    def before_change_value_of(self, element, driver):
        print("before_change_value_of")

    def after_change_value_of(self, element, driver):
        print("after_change_value_of")

    def before_execute_script(self, script, driver):
        print("before_execute_script: " + script)

    def after_execute_script(self, script, driver):
        print("after_execute_script: " + script)

    def before_close(self, driver):
        print("before_close")

    def after_close(self, driver):
        print("after_close")

    def before_quit(self, driver):
        print("before_quit")

    def after_quit(self, driver):
        print("after_quit")

    def on_exception(self, exception, driver):
        print(f"Web Events Exception: " + str(exception))
