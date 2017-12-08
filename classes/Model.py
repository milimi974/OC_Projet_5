#!/usr/bin/env python3.5
# coding: utf-8

# load dependencies
from classes.Database import Database as DB


class Model(object):
    def __init__(self, args={}):
        # init attributes
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
                (DB()).update(self.table, self)
            else:
                # Save data
                # if isset primary key id unset
                self.PK_id = None
                print('Save')
                (DB()).save(self.table, self)

    def find(self, request):
        """ Method search data in bdd

        Method arguments:
        request : dic with actions and fields
        """

    def bulk(self, data, update=False):
        """ method for saving a bulk data

        Keyword arguments:
        data -- list of product fields value
        update -- boolean use active update action
        """

        if not update:
            (DB()).save(self.table, data)
        else:
            (DB()).update(self.table, data)