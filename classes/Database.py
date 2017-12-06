#!/usr/bin/env python
# coding: utf-8

#import dependences
# Mysql packages
import mysql.connector

class Database:
    """ That class connect and manage connection to database"""

    # Connection configurations to database
    config = {
        'user': 'c2python',
        'password': '99#database#99',
        'host': '198.245.49.203',
        'database': 'c2pure_beurre',
        'raise_on_warnings': True,
    }

    def __init__(self):
        pass

    @property
    def connect(self):
        try:
            self.db = mysql.connector.connect(**self.config)
            print('DB connected')
        except:
            print('Error connected')