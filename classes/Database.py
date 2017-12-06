#!/usr/bin/env python
# coding: utf-8

#import dependences
# Mysql packages
import pymysql.cursors

class Database:
    """ That class connect and manage connection to database"""

    def __init__(self):
        self.host = ''
        self.port = 3306
        self.user = ''
        self.passwd = ''
        self.dbname = ''

    @property
    def connect(self):
        try:
            self.db = pymysql.connect(host=self.host,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.dbname,
                             port=self.port)
            print('DB connected')
        except:
            print('Error connected')