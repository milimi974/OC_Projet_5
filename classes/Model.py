#!/usr/bin/env python
# coding: utf-8

""" Module Parent for all class need access to BDD """

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
        if hasattr(self, 'fields') and not self.fields == "" and args:
            for field in self.fields:
                if field in args:
                    setattr(self, field, args[field])

    @property
    def __is_error(self):
        """ Property tell if can send request to bdd """

        # Check if table name set and not empty
        if hasattr(self, 'table') and not self.table == "":
            return False
        return True

    def save(self):
        """ Method save or update data do bdd """
        if not self.__is_error:

            if hasattr(self, 'PK_id') and int(self.PK_id) > 0:
                # Update data
                DB.update(self.table, self.fields, self)
            else:
                # Save data
                # if isset primary key id unset
                self.PK_id = None
                DB.save(self.table, self.fields, self)

    def find(self, request):
        """ Method search multi answer

        Keyword arguments:
        request -- dict of instructions for database request
        """
        return DB.search(self.table, request, False, self.__class__)

    def findone(self, request):
        """ Method search one answer

        Keyword arguments:
        request -- dict of instructions for database request

        """
        return DB.search(self.table, request, True, self.__class__)

    def findjoin(self, table1, request, table2=None):
        """ Method search join answer

        Keyword arguments:
        table1 -- str name of main table for JOIN
        table2 -- str name join table
        request -- dict of instructions for database request

        """
        if not table2:
            table2 = self.table

        return DB.search(table1, request, False, self.__class__, table2)

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

    def search_by(self, args):
        """ Make a search on one field

        Keyword arguments:
        args -- tuple
            (
                field -- str name of database field
                value -- str || list
            )

        """
        request = {
            'fields': 'all',
            'where': [
                args,
            ]
        }
        return DB.search(self.table, request, False, self.__class__)
