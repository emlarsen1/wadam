
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:42:42 2023

@author: Mark Larsen
"""
import sqlite3
from sqlite3 import Error
import datetime
import json
import csv
import pandas as pd
from cfg_log import cfg
from datetime import date


class db():

    def __init__(self):
        try:
            self.conn = sqlite3.connect('wadm.db')
            self.cursor = self.conn.cursor()
            self.user_creds = cfg()
            self.username = self.user_creds.getUserName()

        except Exception as e:
            print(f"Error connecting to database: {e}")

    def update_bannedASIN(self):
        """ create a database connection to a database that resides
            in the memory
        """
        try:

            file = open(
                r"S:\2.5 Regulated Waste\Donations\Food Bank of the Rockies\COpsBannedList.csv")
            contents = csv.reader(file)
            insert_records = "REPLACE INTO copsbanned (ASIN) VALUES (?)"
            self.conn.executemany(insert_records, contents)
            self.conn.commit()
            r_df = pd.read_sql("select * from copsbanned", self.conn)
            print(r_df)

        except Error as e:
            print(e)

    def isBanned(self, ASIN):

        try:
            select_statement = F"SELECT ASIN FROM copsbanned WHERE ASIN = '{ASIN}'"
            self.cursor.execute(select_statement)
            r = self.cursor.fetchone()
            if r is not None:
                return True
            else:
                return False

        except Error as e:
            print(e)

    def addBanned(self, ASIN):

        # Add ASIN to the list
        try:
            insert_statement = f"INSERT OR IGNORE INTO copsbanned(ASIN) VALUES ('{ASIN}')"
            self.cursor.execute(insert_statement)
            r = self.cursor.fetchone()
            if r is not None:
                return True
            else:
                return False
        except Error as e:
            print(e)

    def log_scan_to_csv(self, scan_data):
        # take a list of scan data and write it to a csv file
        try:
            with open(fr'log\{self.username}_{date.today()}_scan_log.csv', 'a', newline='') as scan_log:
                writer = csv.writer(scan_log)
                writer.writerow(scan_data)

        except Exception as e:
            print(e)

    def add_scan(self, barcode, ASIN, pandash, denali, csi_reject, csi_recall, donatable, htrc, hazmat_exception, un_classification, limited_quantity_guidance):

        # Add scan to the list
        self.barcode = barcode
        self.ASIN = ASIN
        self.pandash = pandash
        self.denali = denali
        self.csi_reject = csi_reject
        self.csi_recall = csi_recall
        self.donatable = donatable
        self.htrc = htrc
        self.hazmat_exception = hazmat_exception
        self.un_classification = un_classification
        self.limited_quantity_guidance = limited_quantity_guidance

        # get the current datetime and store it in a variable
        self.scanDateTime = datetime.datetime.now()

        try:
            insert_statement = "INSERT OR IGNORE INTO scans(barcode, ASIN, scan_date, pandash, denali, csi_reject, csi_recall, donatable, htrc, hazmat_exception, un_classification, limited_quantity_guidance)"\
                + f" VALUES ('{self.barcode}','{self.ASIN}','{self.scanDateTime}' , '{self.pandash}', '{self.denali}', '{self.csi_reject}', '{self.csi_recall}', {self.donatable}, {self.htrc}, '{self.hazmat_exception}', '{self.un_classification}', '{self.limited_quantity_guidance}')"
            print(insert_statement)
            scan_result = self.cursor.execute(insert_statement)

            if scan_result is not None:
                self.conn.commit()
                print(f"log record: {scan_result}")
                # Add scan to the list
                scan_data = []
                scan_data.append(self.barcode)
                scan_data.append(self.ASIN)
                scan_data.append(self.scanDateTime)
                scan_data.append(self.pandash)
                scan_data.append(self.denali)
                scan_data.append(self.csi_reject)
                scan_data.append(self.csi_recall)
                scan_data.append(self.donatable)
                scan_data.append(self.htrc)
                scan_data.append(self.hazmat_exception)
                scan_data.append(self.un_classification)
                scan_data.append(self.limited_quantity_guidance)
                self.log_scan_to_csv(scan_data)
                print(f"Scan logged: {self.ASIN}")
                # TODO: add copy to server & delete / import any from server need to not duplicate imports.. how do we do this
                # \\ant\dep-na\DEN2\Support\Safety\2.5 Regulated Waste\Processing Assist\log\
                return True
            else:
                print("No scan logged")
                return False
        except Error as e:
            print(f"Error logging scan: {e}")

    def get_scan(self, barcode):

        # Add scan to the list
        self.barcode = barcode

        try:

            select_statement = f"SELECT  * FROM  scans s WHERE barcode = '{barcode}' or ASIN = '{barcode}'"
            result: list[sqlite3.Row] = self.cursor.execute(
                select_statement).fetchone()
            if result is not None:
                print(result)
                self.cursor.row_factory = None
                return result
            else:
                print("No previous scan found")
                self.cursor.row_factory = None
                return False
        except Error as e:
            self.cursor.row_factory = None
            print(e)

    def __del__(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        print('Destructor called, db closed.')
