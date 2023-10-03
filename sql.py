
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:42:42 2023

@author: Mark Larsen
"""
import sqlite3
from sqlite3 import Error
import csv
import pandas as pd


class db():

    def __init__(self):
        self.conn = sqlite3.connect('wadm.db')
        self.cursor = self.conn.cursor()

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

    def add_scan(self, barcode, ASIN, pandash, denali, csi_reject, csi_recall):

        # Add scan to the list
        self.barcode = barcode
        self.ASIN = ASIN
        self.pandash = pandash
        self.denali = denali
        self.csi_reject = csi_reject
        self.csi_recall = csi_recall

        try:
            insert_statement = f"INSERT OR IGNORE INTO scans(barcode, ASIN, pandash, denali, csi_reject, csi_recall)\
                VALUES ('{self.barcode}','{self.ASIN}', '{self.pandash}', '{self.denali}', '{self.csi_reject}', '{self.recall}')"
            self.cursor.execute(insert_statement)
            r = self.cursor.fetchone()
            if r is not None:
                return True
            else:
                return False
        except Error as e:
            print(e)

    def get_scan(self, barcode):

        # Add scan to the list
        self.barcode = barcode

        try:
            select_statement = f"SELECT  * FROM  scans s WHERE barcode = '{barcode}' or ASIN = '{barcode}'"
            self.cursor.execute(select_statement)
            r = self.cursor.fetchone()
            if r is not None:
                return True
            else:
                return False
        except Error as e:
            print(e)

    def __del__(self):
        self.conn.close()
        print('Destructor called, db deleted.')
