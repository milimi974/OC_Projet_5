#!/usr/bin/env python
# coding: utf-8

#import dependences
# Mysql packages
import pymysql.cursors

class Database:
    """ That class connect and manage connection to database"""

    def __init__(self, **kwargs):
        self.host = kwargs.host
        self.port = kwargs.port
        self.user = kwargs.user
        self.passwd = kwargs.passwd

    def connect(self):
        pass