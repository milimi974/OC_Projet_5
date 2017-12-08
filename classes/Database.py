#!/usr/bin/env python3.5
# coding: utf-8

# import dependencies
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

    # var contain instance of DB
    __instance = None

    def __new__(cls):
        """ Defined the class has Singleton """
        # Control attribute name if instance doesn't exist return nes instance

        if Database.__instance is None:
            Database.__instance = object.__new__(cls)
            # Init db attribute
            Database.__instance.db = False
            Database.__instance.connected = False
            # Connect instance self.db to DB
            Database.__instance.__connect
        return Database.__instance

    @staticmethod
    def save(tablename, fields, data):
        """ Method save data in database

        Keyword arguments:
        tablename -- string name of table
        data -- object or [object] to save

        """
        DB = Database()
        query = DB.cursor
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        if 'PK_id' in fields:
            fields.remove('PK_id')
        prepare = ['%s' for n in fields]
        req = ('INSERT INTO {} ({}) VALUES ({})'.format(tablename, ','.join(fields), ','.join(prepare)))


        if type(data) == list:
            q = []
            for d in data:
                args = d.__dict__
                p = []
                for field in fields:
                    p.append(args[field])
                q.append(tuple(p))

            query.executemany(req,q)
        else:
            p = []
            for field in fields:
                p.append(data[field])
            query.execute(req, tuple(p))

        DB.cnx.commit()
        query.close()

    @staticmethod
    def update(tablename, fields, data):
        """ Method update data in database

        Keyword arguments:
        tablename -- string name of table
        data -- object or [object] to update

        """
        DB = Database()
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False

    @staticmethod
    def select(tablename, conditions):
        """ Method save data in database

        Keyword arguments:
        tablename -- string name of table
        conditions -- dict of conditions to apply on request

        """
        DB = Database()
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False

    @staticmethod
    def query(tablename, request):
        """ Method save data in database

        Keyword arguments:
        tablename -- string name of table
        request -- string a sql request

        """
        DB = (Database())
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False

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
        return self.connected

    @property
    def cursor(self):
        """ Return connection cursor """
        return self.db.cursor()

    @property
    def cnx(self):
        """ Return connection """
        return self.db