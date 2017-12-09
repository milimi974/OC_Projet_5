#!/usr/bin/env python3
# coding: utf-8

# load dependencies
from classes.Database import Database as DB


class Model(object):
    """ That Class manage method for BDD """

    def __init__(self, args={}):
        """ Constructor

        Method arguments:
        args -- dict object attribute value

        """
        # init attributes
        self.PK_id = None
        if hasattr(self, 'fields') and not self.fields == "":
            for field in self.fields:
                if field in args:
                    setattr(self, field, args[field])

    @property
    def __is_error(self):
        """ Property tell if can send request to bdd """

        # Check if table name set and not empty
        if hasattr(self, 'table') and not self.table == "":
            return False
        else:
            return True

    def save(self):
        """ Method save or update data do bdd """
        if not self.__is_error:
            # copy instance attribute in dictionary
            args = dict(self.__dict__)

            if hasattr(self, 'PK_id') and int(self.PK_id) > 0:
                # Update data
                print('Update')
                DB.update(self.table, self.fields, self)
            else:
                # Save data
                # if isset primary key id unset
                self.PK_id = None
                print('Save')
                DB.save(self.table, self.fields, self)

    def find(self, request, one=False):
        """ Method search data in bdd

        Method arguments:
        request : dict with actions and fields
        {
            'fields':'all or ['field',]',
            'where': tuple ('field %cond%': %value% / [list of tuple] / (tuple) , ),
            'order': ['field',], str || list
            'group': ['field',],
            'limit': [int,int],

        }
        %cond% -- =, >, <, >=, <=, IN, BETWEEN, LIKE,
        %value%  -- IS NULL, IS NOT NULL
        """
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
        if type(request['where']) == list:
            for element in request['where']:
                conditions += self.__format_where(*element)

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
        return DB.select(self.table,fields, conditions, one, others)


    def __format_where(self, field, value):
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
                            d.append(self.__make_condition('', a, b))
                    else:
                        d.append(self.__make_condition('', x, y))

                conditions += ' ' + field + ' (' + link.join(d) + ')'
            else:
                x, y = value
                conditions += self.__make_condition(field, x, y)

        else:
            conditions += self.__make_condition('AND', field, value)

        return conditions

    @staticmethod
    def __make_condition(link, key, value):
        """ Static method format one condition where"""

        # extract condition on field
        act = key.split()
        # if no condition set add =
        if len(act) == 1:
            if type(value) == str:
                if not value == 'IS NULL' and not value == 'IS NOT NULL':
                    act.append('=')

        # Action on special condition
        if act[1] == 'IN':
            value = '({})'.format(','.join(value))
        elif act[1] == 'BETWEEN':
            value = '{} AND {}'.format(str(value[0]), str(value[1]))
        elif act[1] == 'LIKE' or type(value) == str:
            value = "'{}'".format(value)
        # Return formated condition
        return '{} {} {} {} '.format(link, act[0], act[1], str(value))

    def bulk(self, data, update=False):
        """ method for saving a bulk data

        Keyword arguments:
        data -- list of product fields value
        update -- boolean use active update action
        """

        if not update:
            # Call method for save data
            DB.save(self.table, self.fields, data)
        else:
            # Call method for update data
            DB.update(self.table, self.fields, data)

    def search_by(self, field, value):
        pass
