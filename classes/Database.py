#!/usr/bin/env python
# coding: utf-8

# import dependences
# Mysql packages
import mysql.connector


class Database:
    """ That class connect and manage connection to database"""

    # Connection configurations to database
    # Class attributes
    config = {
        'user': 'c2python',
        'password': '99#database#99',
        'host': '198.245.49.203',
        'database': 'c2pure_beurre',
        'raise_on_warnings': True,
    }

    def __init__(self):
        """ Constructor initialise instance attributes """
        self.db = False

    @property
    def connect(self):
        """ Property connect instance to Database """

        # Exception try to connect Database
        try:
            self.db = mysql.connector.connect(**self.config)
            print('DB connected')
        except:
            print('Error connected')