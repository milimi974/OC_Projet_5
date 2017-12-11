#!/usr/bin/env python
# coding: utf-8

# Import Model parent
from classes.Model import Model
from classes.Functions import *

class Shop(Model):
    """ Class associate table Shops """

    # Database table name
    table = 'Shops'

    # Fields name on db
    fields = [
        'PK_id',
        'name',
        'uri',
    ]

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__(args)

        if 'name' in args:
            self.uri = serialized_title(args['name'])

    def get_shops(self, ID):
        """ Method return all shops for one food

        Keyword arguments:
        ID -- int food ID

        """
        args = {
            'where': [
                ('Food_has_Shops.FK_food_id =', int(ID))
            ],
            'on': [
                ('Shops.PK_id =', 'Food_has_Shops.FK_shop_id'),
            ]
        }
        return self.findjoin('Food_has_Shops', args)

    @property
    def _get_name(self):
        """ property return object attribute name"""
        return self.name