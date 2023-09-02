# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 02:26:57 2023

@author: Mark Larsen
"""

import configparser
import os
from os import path


class cfg():

    def __init__(self):
        # variables
        self.config = configparser.ConfigParser()

        self.userName = "UserName"
        self.userPassword = "Password"
        self.userBadgeID = "Badge ID"
        self.userPin = "Pin Code"
        self.userSiteID = "SiteID"
        self.userRememberMe = str(1)
        self.FBAOverride = str(1)
        self.xpos = str(10)
        self.ypos = str(10)
        self.localAppData = str(os.getenv("LOCALAPPDATA"))

        iniFile = os.path.join(self.localAppData, "WADAM", "wadam.ini")
        print(iniFile)
        if path.isfile(iniFile):
            print('ini file exists')

            # Read ini file
            self.config.read(iniFile)
            cfgUser = self.config["userInfo"]

            # decode password & Pin Code
            self.userPassword = ''.join(chr(ord(char)-3)
                                        for char in cfgUser["pass"]).strip()
            self.userPin = ''.join(chr(ord(char)-3)
                                   for char in cfgUser["pincode"]).strip()

            self.userName = cfgUser["User"]
            self.userBadgeID = cfgUser["Badgeid"]
            self.userSiteID = cfgUser["siteid"]
            self.userRememberMe = cfgUser["rememberme"]

            cfgApp = self.config["appInfo"]
            self.fbaoverride = cfgApp["fbaoverride"]
            self.xpos = cfgApp["xpos"]
            self.ypos = cfgApp["ypos"]

        else:
            # Create the file and add headings
            print('ini file does not exist')
            # Encrypt the password. This is extremely week encryption
            # but the file will be stored in the users home directory
            # and only accessible if you are logged in as the user already.
            self.userPassword = ''.join(chr(ord(char)+3)
                                        for char in self.userPassword)
            self.userPin = ''.join(chr(ord(char)+3)
                                   for char in self.userPin)

            self.config.add_section('userInfo')
            self.config.set("userInfo", 'user', self.userName)
            self.config.set("userInfo", 'pass', self.userPassword)
            self.config.set("userInfo", 'badgeid', self.userBadgeID)
            self.config.set("userInfo", 'pincode', self.userPin)
            self.config.set("userInfo", 'siteid', self.userSiteID)
            self.config.set("userInfo", 'rememberme', self.userRememberMe)

            self.config.add_section('appInfo')
            self.config.set("appInfo", 'fbaoverride', str(1))
            self.config.set("appInfo", 'xpos', str(0))
            self.config.set("appInfo", 'ypos', str(0))

            # SAVE CONFIG FILE
            appDirectory = "WADAM"
            parentDirectory = str(os.getenv('LOCALAPPDATA'))
            appPath = os.path.join(parentDirectory, appDirectory)
            os.mkdir(appPath)
            iniFile = str(os.path.join(appPath, "wadam.ini"))
            print(iniFile)
            with open(iniFile, 'w') as configfileObj:
                self.config.write(configfileObj)
                configfileObj.flush()
                configfileObj.close()

    def getUserName(self):
        return self.userName

    def getUserPassword(self):
        return self.userPassword

    def getUserBadgeID(self):
        return self.userBadgeID

    def getUserPinCode(self):
        return self.userPin

    def getUserSiteID(self):
        return self.userSiteID

    def getUserRememberMe(self):
        return self.userRememberMe

    def getWinXpos(self):
        return self.xpos

    def getWinYpos(self):
        return self.ypos

    def saveSiteID(self, dlgSiteID):
        # Save user info to ini settings file
        self.config.set("userInfo", 'siteid', str(dlgSiteID))

        iniFile = os.path.join(
            str(os.getenv('LOCALAPPDATA')), "WADAM", "wadam.ini")
        with open(iniFile, 'w') as cfgFile:
            self.config.write(cfgFile)

    def saveAppInfo(self, xpos, ypos, FBAOverride):
        self.config.set("appInfo", 'fbaoverride', FBAOverride)
        self.config.set("appInfo", 'xpos', xpos)
        self.config.set("appInfo", 'ypos', ypos)

        iniFile = os.path.join(
            str(os.getenv('LOCALAPPDATA')), "WADAM", "wadam.ini")
        with open(iniFile, 'w') as cfgFile:
            self.config.write(cfgFile)

    def saveUser(self, dlgUserName, dlgUserPassword,
                 dlgUserBadgeID, dlgUserPin, dlgRememberMe):
        # Save user info to ini settings file
        # encrypt password & store variables
        self.userPassword = dlgUserPassword
        dlgUserPassword = ''.join(chr(ord(char)+3)
                                  for char in dlgUserPassword)
        self.userPin = dlgUserPin
        dlgUserPin = ''.join(chr(ord(char)+3)
                             for char in dlgUserPin)

        self.userName = dlgUserName
        self.userBadgeID = dlgUserBadgeID
        self.userRememberMe = dlgRememberMe

        self.config.set("userInfo", 'user', str(self.userName))
        self.config.set("userInfo", 'pass', str(dlgUserPassword))
        self.config.set("userInfo", 'badgeid', str(self.userBadgeID))
        self.config.set("userInfo", 'pincode', str(dlgUserPin))
        self.config.set("userInfo", 'rememberme', str(self.userRememberMe))

        # Save the config file
        try:
            iniFile = os.path.join(
                str(os.getenv('LOCALAPPDATA')), "WADAM", "wadam.ini")
            with open(iniFile, 'w') as cfgFile:
                self.config.write(cfgFile)
            return True
        except Exception as e:
            print(e)
            return False

    def openConfig(self):
        osCommandString = f"notepad.exe {os.path.join(str(os.getenv('LOCALAPPDATA')), 'WADAM', 'wadam.ini')}"
        os.system(osCommandString)
