#!/usr/bin/env python
# coding: utf-8

# import dependences
# Mysql packages
import mysql.connector


class Database(object):
    """ That class connect and manage connection to database
        and inherit object parent
    """

    # Connection configurations to database
    # Class attributes
    config = {
        'user': 'c1python',
        'password': '99#database#99',
        'host': '198.245.49.203',
        'database': 'c1python',
        'raise_on_warnings': True,
    }

    def __new__(cls):
        """ Defined the class has Singleton """
        # Control attribute name if instance doesn't exist return nes instance

        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """ Constructor initialise instance attributes """

        # Init db attribute
        self.db = False
        self.connected = False
        # Connect instance self.db to DB
        self.__connect

    @property
    def __connect(self):
        """ Property connect instance to Database """

        # Exception try to connect Database
        try:
            self.db = mysql.connector.connect(**self.config)
            print('DB connected')
            self.connected = True

        except:
            print('Error connected')
            self.connected = False

    @property
    def is_connected(self):
        """ Return connection status """
        return self.is_connected
