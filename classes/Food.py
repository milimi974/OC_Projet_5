#!/usr/bin/env python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.Category import Category
from classes.Shop import Shop


# Import Model parent
from classes.Model import Model
from classes.Functions import *


class Food(Model):
    """ Manage food database """

    # Database table name
    table = 'Foods'
    # Table column names
    fields = [
        'PK_id',
        'code',
        'uri',
        'link',
        'name',
        'description',
        'level',
        'created',
        'modified',
    ]

    def __init__(self, args={}):
        """ Initialized Food object

        Keyword arguments:
        args -- list of product fields value

        """
        # Instantiate Parent
        super().__init__(args)

        if args:
            if int(self.PK_id) > 0:
                self.categories = (Category()).get_categories(self.PK_id)
                self.shops = (Shop()).get_shops(self.PK_id)
            else:
                self.uri = serialized_title(args['name'])

                # init attributes
                if 'categories' in args:
                    self.categories = self.__make_categories(args['categories'])
                if 'shops' in args:
                    self.shops = self.__make_shops(args['shops'])

    def __make_categories(self,categories):
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

    def __make_shops(self,shops):
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

    def bulk(self, data, update=False, names=[]):
        """ Override parent method

        Keyword arguments:
        data -- list of product fields value
        update -- boolean use active update action
        names -- list contain uri foods name

        """
        print("Bulk child")
        # Call parent method
        Model.bulk(data, update)
        if not update:
            # Add foods
            db_data = (Food()).search_by(('uri IN', names))
            # List of categories ids created
            cat_ids = []
            cat_names = []
            for cat in data.categories.items():
                cat_names.append(cat.name)

            if cat_names:
                db_cat = (Category()).search_by(('name IN', names))

        else:
            # Update Foods
            pass

    @property
    def _get_name(self):
        """ property return object attribute name"""
        return self.name