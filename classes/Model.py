#!/usr/bin/env python3.5
# coding: utf-8

# load dependences
from classes.Database import Database as DB


class Model(object):
    def __init__(self):
        pass

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
            # copie instance attribute in dictionary
            args = dict(self.__dict__)

            if hasattr(self, 'PK_id') and int(self.PK_id) > 0:
                # Update data
                print('Update')
            else:
                # Save data
                if hasattr(self, 'PK_id'):
                    # if isset primary key id unset
                    del args['PK_id']

                print('Save')

    def find(self, request):
        """ Method search data in bdd

        Method arguments:
        request : dic with actions and fields
        """

    def get_table(self):
        print(self.table)
        print(self.__dict__)