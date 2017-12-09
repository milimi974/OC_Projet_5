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
        # Remove primary key
        if 'PK_id' in fields:
            fields.remove('PK_id')
        # Prepare request
        prepare = ['%s' for n in fields]
        req = ('INSERT INTO {} ({}) VALUES ({})'.format(tablename, ','.join(fields), ','.join(prepare)))

        # Format values for prepared request
        if type(data) == list:
            q = []
            for d in data:
                args = d.__dict__
                p = []
                # Extract form data only field configs for change
                # and create new list in the right order
                for field in fields:
                    p.append(args[field])
                q.append(tuple(p))
            # Bulk insert data
            query.executemany(req,q)
        else:
            p = []
            args = data.__dict__
            for field in fields:
                p.append(args[field])
            # Unique insert data
            query.execute(req, tuple(p))
        # Send request to database
        DB.cnx.commit()
        # Close query
        query.close()

    @staticmethod
    def update(tablename, fields, data):
        """ Method update data in database

        Keyword arguments:
        tablename -- string name of table
        data -- object or [object] to update

        """

        DB = Database()
        query = DB.cursor
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        # Remove primary key
        if 'PK_id' in fields:
            fields.remove('PK_id')

        # Format values for prepared request
        if type(data) == list:
            for d in data:
                Database.__up(tablename, fields, d.__dict__)
        else:
            Database.__up(tablename, fields, data.__dict__)

        # Send request to database
        DB.cnx.commit()
        # Close query
        query.close()

    @staticmethod
    def __up(tablename, fields, args):
        """ Static Method update data

        Keyword arguments:
        tablename -- string name of table
        fields -- list of fields name of table
        args -- dict of fields an value to update

        """
        p = []
        # Extract form data only field configs for change
        for field in fields:
            p.append(args[field])
        # Create conditional on primary key
        if 'PK_id' in args and int(args['PK_id']) > 0:
            cond = 'PK_id = ' + str(args['PK_id'])

        # Prepare request
        prepare = [n + ' = %s' for n in fields]
        req = tuple('UPDATE {} SET {} WHERE {}'.format(tablename, ','.join(prepare), cond))
        query =(Database()).cursor
        # Unique insert data
        query.execute(req, tuple(p))

    @staticmethod
    def select(tablename, fields, conditions, one=False, others=[]):
        """ Method return data form database

        Keyword arguments:
        tablename -- string name of table
        fields -- database fields name for request or * for all
        conditions -- dict of conditions to apply on request
        one -- boolean use for return only one answer
        others -- dict of complements information request

        """
        DB = Database()
        query = DB.cursor

        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        # Format if fields selected
        if not fields == '*':
            fields = ','.join(fields)

        req = 'SELECT {} FROM {} WHERE {} {}'.format(fields,tablename,conditions,others)

        query.execute(req)
        if one:
            return query.fetchone()
        return query.fetchall()

    @staticmethod
    def query(tablename, request):
        """ Method save data in database

        Keyword arguments:
        tablename -- string name of table
        request -- string a sql request

        """
        DB = (Database())
        _query = DB.cursor
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        _query.execute(request)
        rows = _query.fetchall()
        insertID = _query.lastrowid
        # Send request to database
        DB.cnx.commit()
        # Close query
        _query.close()

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
        """ Return connection cursor for execute request"""
        return self.db.cursor()

    @property
    def cnx(self):
        """ Return connection """
        return self.db