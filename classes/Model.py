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
        setattr(self, 'PK_id', 0)
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
            fields = list(self.fields)
            table = str(self.table)
            if hasattr(self, 'PK_id') and int(self.PK_id) > 0:
                # Update data
                DB.update(table, fields, self)
            else:
                # Save data
                # if isset primary key id unset
                self.PK_id = None
                DB.save(table, fields, self)

    def find(self, request):
        """ Method search multi answer

        Keyword arguments:
        request -- dict of instructions for database request

        """

        table = str(self.table)
        return DB.search(table, request, False, self.__class__)

    def findone(self, request):
        """ Method search one answer

        Keyword arguments:
        request -- dict of instructions for database request

        """

        table = str(self.table)
        return DB.search(table, request, True, self.__class__)

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

    def bulk(self, data, update=False, tablename=None, fields=None):
        """ method for saving a bulk data

        Keyword arguments:
        data -- list of product fields value
        update -- boolean use active update action
        -- for join table --
        tablename -- string custom table
        fields -- custom fields
        """
        if not tablename:
            tablename = str(self.table)

        if not fields:
            fields = list(self.fields)

        if not update:
            # Call method for save data
            DB.save(tablename, fields, data)
        else:
            # Call method for update data
            DB.update(tablename, fields, data)


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
        table = str(self.table)
        return DB.search(table, request, False, self.__class__)

    def search_ids(self, args):
        """ Make a search on one field

        Keyword arguments:
        args -- tuple
            (
                field -- str name of database field
                value -- str || list
            )

        """
        request = {
            'fields': 'PK_id',
            'where': [
                args,
            ]
        }
        table = str(self.table)
        rep = DB.search(table, request, False, self.__class__)
        ids = []
        if rep:
            for el in rep:
                ids.append(el.PK_id)
        return ids

    def search_id(self, args):
        """ Make a search on one field then return PK_id

        Keyword arguments:
        args -- tuple
            (
                field -- str name of database field
                value -- str || list
            )

        """
        request = {
            'fields': 'PK_id',
            'where': [
                args,
            ]
        }
        table = str(self.table)
        rep = DB.search(table, request, True, self.__class__)

        if rep:
            return rep.PK_id
        return False

    def get_list(self, fields, request):
        """ Return a dict with key:value

        Keyword arguments:
        fields -- tuple for dict key value
        request -- tuple search request conditions
        """
        query = self.search_by(request)

        rep = []
        key, value = fields
        for el in query:
            rep.append((el.__getattribute__(key),el.__getattribute__(value)))
        return rep

    def delete(self, request):
        """ delete element from data base """
        table = str(self.table)
        DB.delete(table, request)