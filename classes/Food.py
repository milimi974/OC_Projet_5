#!/usr/bin/env python
# coding: utf-8

# load dependences
# Import classes packages
from classes.Category import Category
from classes.Shop import Shop


# Import Model parent
from classes.Model import Model


class Food(Model):
    """ Manage food database """

    # Database table name
    table = 'Foods'

    def __init__(self,args):
        """ Initialized Food object

        Keyword arguments:
        args -- list of product fields value

        """
        # Instanciate Parent
        super().__init__()

        # init attributes
        self.PK_id = args['PK_id']
        self.code = args['code']
        self.link = args['link']
        self.name = args['name']
        self.description = args['description']
        self.level = args['level']
        self.created = args['created']
        self.modified = args['modified']

        self.categories = self.__add_categories(args['categories'])
        self.shops = self.__add_shops(args['shops'])


    def __add_categories(self,categories):
        """ create a new category object then add to attribute list

        Keyword arguments:
        categories -- string of product categories

        """

        # responses var
        response = []
        # test type of value if string
        if type(categories) is str:
            # Make a list with string
            categories = categories.split(',')
            # for each category remove term en and pl
            for category in categories:
                if 'en:' not in category and 'pl:' not in category:
                    response.append(Category(category))
        return response

    def __add_shops(self,shops):
        """ create a new shop object then add to attribute list

        Keyword arguments:
        shops -- string of product stores

        """

        # responses var
        response = []
        # test type of value if string
        if type(shops) is str:
            # Make a list with string
            shops = shops.split(',')
            for shop in shops:
                response.append(Shop(shop))
        return response
