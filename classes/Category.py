#!/usr/bin/env python3.5
# coding: utf-8

# Import Model parent
from classes.Model import Model
from classes.Functions import *

class Category(Model):
    """ Class associate to table categories """

    # Database table name
    table = 'Categories'

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

    def get_categories(self, ID):
        """ Method return all categories for one food

        Keyword arguments:
        ID -- int food ID

        """
        args = {
            'where': [
                ('Food_has_Categories.FK_food_id =',int(ID))
            ],
            'on': [
                ('Categories.PK_id =', 'Food_has_Categories.FK_categorie_id'),
            ]
        }
        return self.findjoin('Food_has_Categories',args)

