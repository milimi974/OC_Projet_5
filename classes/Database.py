#!/usr/bin/env python
# coding: utf-8

""" Module Parent for request to BDD """

# import dependencies
from classes.Functions import *

# Mysql packages
import mysql.connector
from mysql.connector import Error

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
            Database.__instance.format_fields = []
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

        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        query = DB.cursor
        # Remove primary key
        if 'PK_id' in fields:
            fields.remove('PK_id')
        # Prepare request
        prepare = ['%s' for n in fields]
        req = ('INSERT INTO {} ({}) VALUES ({})'
               .format(tablename,
                       ','.join(fields),
                       ','.join(prepare)))

        # return object answer
        response = False

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
            try:

                query.executemany(req, q)
                response = True
            except Error as e:
                print(e)
                print(req)
                print(q)

        else:
            p = []
            args = data.__dict__
            for field in fields:
                p.append(args[field])
            # Unique insert data
            try:
                query.execute(req, tuple(p))
                response = query.lastrowid
            except Error as e:
                print(e)
                print(req)
                print(p)

        # Send request to database
        DB.cnx.commit()
        # Close query
        query.close()

        return response

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
                DB.__up(tablename, fields, d.__dict__)
        else:
            DB.__up(tablename, fields, data.__dict__)

        # Send request to database
        DB.cnx.commit()
        # Close query
        query.close()

    def __up(self, tablename, fields, args):
        """ Static Method update data

        Keyword arguments:
        tablename -- string name of table
        fields -- list of fields name of table
        args -- dict of fields an value to update

        """
        p = []
        # Extract form data only field configs for change
        for field in fields:
            p.append(clear_texte(args[field]))
        # Create conditional on primary key
        if 'PK_id' in args and int(args['PK_id']) > 0:
            cond = 'PK_id = ' + str(args['PK_id'])

            # Prepare request
            prepare = [n + ' = %s' for n in fields]
            req = ('UPDATE {} SET {} WHERE {}'.format(tablename, ','.join(prepare), cond))

            query = Database().cursor
            # Unique insert data
            try:
                query.execute(req, p)
            except:
                print(req)
                print(p)

            Database().cnx.commit()
            # Close query
            query.close()

    @staticmethod
    def search(format_fields, tablename, request, one, classname, jointable=''):
        """ Method search data in bdd

        Method arguments:
        format_fields -- dict field format
        tablename -- str name of table
        one -- boolean True one response
        classname -- obj for build response
        jointable -- str name table for JOIN request
        request : dict with actions and fields
        {
            'fields':'all or ['field',]',
            'where': [tuple ('field %cond%': %value% / [list of tuple] / (tuple) , )],
            'order': ['field',], str || list
            'group': ['field',],
            'limit': [int,int],

        }
        %cond% -- =, >, <, >=, <=, IN, BETWEEN, LIKE,
        %value%  -- IS NULL, IS NOT NULL

        """
        # set format field on object
        Database().format_fields = format_fields

        # Format fields
        fields = '*'
        if 'fields' in request:
            if type(request['fields']) == str:
                if not request['fields'] == 'all':
                    fields = request['fields']
            elif type(request['fields']) == list:
                fields = ','.join(request['fields'])

        # Format where
        conditions = '1=1 '
        if 'where' in request and type(request['where']) == list:
            for element in request['where']:
                conditions += Database().__format_where(*element)

        # Format join
        joins = ''
        if 'on' in request and type(request['on']) == list:
            req = ''
            for element in request['on']:
                field, value = element
                req += Database().__format_where(field, value, True)
            req = req[3:]
            joins = ' LEFT JOIN {} ON {} '.format(jointable, req)

        # Format orders
        others = ''
        if 'order' in request:
            if type(request['order']) == list:
                others += ' ORDER BY ' + ','.join(request['order'])
            else:
                others += ' ORDER BY ' + str(request['order'])

        # Format group
        if 'group' in request:
            if type(request['group']) == list:
                others += ' GROUP BY ' + ','.join(request['group'])
            else:
                others += ' GROUP BY ' + str(request['group'])

        # Format Limit
        if 'limit' in request:
            if type(request['limit']) == list:
                others += ' LIMIT ' + ','.join(str(e) for e in request['limit'])
            else:
                others += ' LIMIT ' + str(request['limit'])

        # Request answer
        response = Database().select(tablename, fields, conditions, one, others, joins)

        response = Database().__decode_rep(response)
        rep = []
        # Format answer in class object
        if type(response) == list:
            for el in response:
                rep.append(classname(el))
        else:
            rep = classname(response)

        Database().format_fields = []
        return rep

    def __decode_rep(self, response):
        """ decoding str from db
        Method arguments:
        response -- list || dict data from db
        """
        rep = []
        if self.format_fields:
            if type(response) == list:
                for el in response:
                    x = {}
                    for key, value in el.items():
                        x[key] = decode_field(self.format_fields, key, value)
                    rep.append(x)
            else:
                rep = {}
                for key, value in response.items():
                    rep[key] = decode_field(self.format_fields, key, value)
        return rep

    def __format_where(self, field, value, join=False):
        """ Format element on where conditions

        Method arguments:
        field -- str name of field or condition AND || OR
        value -- tuple || list

        """

        conditions = ''

        if field == 'OR' or field == 'AND':
            if type(value) == list:
                link = 'AND'
                d = []
                for el in value:
                    x, y = el
                    if x == 'OR' or x == 'AND':
                        link = x
                        for el2 in y:
                            a, b = el2
                            d.append(self.__make_condition('', a, b, join))
                    else:
                        d.append(self.__make_condition('', x, y, join))

                conditions += ' ' + field + ' (' + link.join(d) + ')'
            else:
                x, y = value
                conditions += self.__make_condition(field, x, y, join)

        else:
            conditions += self.__make_condition('AND', field, value, join)

        return conditions

    def __make_condition(self, link, key, value, join=False):
        """ Static method format one condition where

        Method arguments:
        link -- str AND || OR
        key -- str field name + condition
        value -- ??
        join -- boolean for join request
        """

        # extract condition on field
        act = key.split()

        # if no condition set add =
        if len(act) == 1:
            if type(value) == str:
                if not value == 'IS NULL' and not value == 'IS NOT NULL':
                    act.append('=')

        # Action on special condition
        if len(act) >= 2:
            if act[1] == 'IN':
                if type(value) == list:
                    if type(value[0]) == str:
                        value = '({})'.format(
                            ','.join(["'" +
                                      parse_field(self.format_fields, act[0], a) +
                                      "'" for a in value]))
                    else:
                        value = '({})'.format(','.join([str(el) for el in value]))
            elif act[1] == 'BETWEEN':
                value = '{} AND {}'.format(
                    parse_field(self.format_fields, act[0], value[0]),
                    parse_field(self.format_fields, act[0], value[1]))
            elif act[1] == 'LIKE':
                value = "'{}'".format(str(parse_field(self.format_fields, act[0], value)))
            elif type(value) == str and not join:
                # Return format condition
                value = "'{}'".format(parse_field(self.format_fields, act[0], value))

            return '{} {} {} {} '.format(link, act[0], act[1], value)
        return '{} {} {} '.format(link, act[0], value)

    @staticmethod
    def select(tablename, fields, conditions, one=False, others=[], joins=''):
        """ Method return data form database

        Keyword arguments:
        tablename -- string name of table
        fields -- database fields name for request or * for all
        conditions -- dict of conditions to apply on request
        one -- boolean use for return only one answer
        others -- dict of complements information request

        """

        DB = Database()

        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        query = DB.cnx.cursor(dictionary=True, buffered=True)
        # Format if fields selected
        if not fields == '*' and type(fields) == list:
            fields = ','.join(fields)

        req = 'SELECT {} FROM {} {} WHERE {} {}'\
            .format(fields,
                    tablename,
                    joins,
                    conditions,
                    others)

        try:
            query.execute(req)
        except:
            print(req)


        rep = []
        if query.rowcount > 0:
            if one:
                rep = query.fetchone()
            else:
                rep = query.fetchall()

        Database().cnx.commit()
        # Close query
        query.close()
        return rep

    @staticmethod
    def query(request):
        """ Method save data in database

        Keyword arguments:
        request -- string a sql request

        """
        DB = (Database())
        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False
        _query = (DB.cnx).cursor(dictionary=True, buffered=True)
        _query.execute(request)
        insertID = _query.lastrowid
        rows = []
        if _query.rowcount > 0:
            rows = _query.fetchall()

        # Send request to database
        DB.cnx.commit()
        # Close query
        _query.close()

        if insertID:
            return insertID
        return rows

    @staticmethod
    def delete(tablename, request):
        """ Method delete data form database

        Keyword arguments:
        tablename -- string name of table
        request -- dict of conditions to apply on request

        """

        DB = Database()

        # if doesn't connected to db break
        if not DB.is_connected:
            print('Error connected')
            return False

        query = DB.cnx.cursor(dictionary=True, buffered=True)

        # Format where
        conditions = ''
        if 'where' in request and type(request['where']) == list:
            for element in request['where']:
                conditions += Database().__format_where(*element)
            # Remove AND in condition
            conditions = conditions[3:]

        req = 'DELETE FROM {} WHERE {}' \
            .format(tablename,
                    conditions)
        try:
            query.execute(req)
        except:
            print(req)

        Database().cnx.commit()
        # Close query
        query.close()

    def _set_format_fields(self, value):
        """ setters on format_fields attr """
        self.format_fields = value

    def _get_format_fields(self):
        """ getters return format fields """
        return self.format_fields

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
        """ Return connection cursor for execute request """
        if self.is_connected:
            return self.db.cursor()

    @property
    def cnx(self):
        """ Return connection """
        return self.db
