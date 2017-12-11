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
            if self.PK_id and self.PK_id > 0:
                self.categories = (Category()).get_categories(self.PK_id)
                self.shops = (Shop()).get_shops(self.PK_id)
            else:

                if 'name' in args:
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
        if type(categories) is str and categories:
            # Make a list with string
            categories = categories.split(',')
            # for each category remove term en and pl
            for category in categories:
                if 'en:' not in category and 'pl:' not in category:
                    response.append(Category({'name': category}))

        return response

    def __make_shops(self,shops):
        """ create a new shop object then add to attribute list

        Keyword arguments:
        shops -- string of product stores

        """

        # responses var
        response = []
        # test type of value if string
        if type(shops) is str and shops:
            # Make a list with string
            shops = shops.split(',')
            for shop in shops:
                response.append(Shop({'name': shop}))
        return response

    def bulk(self, data, update=False):
        """ Override parent method

        Keyword arguments:
        data -- list of product fields value
        update -- boolean use active update action
        names -- list contain uri foods name

        """
        print("Bulk child")
        # Call parent method
        Model.bulk(self,data, update)
        if not update:
            # List of food categories to create
            food_has_cat = []

            # List of food Shops to create
            food_has_shop = []

            # Loop for each food data
            for food in data:
                # List of food categories to create
                food_has_cat = self.__make_food_category(food)

                # List of food Shops to create
                food_has_shop = self.__make_food_shop(food)

            # Add foods categories
            if len(food_has_cat) > 0:
                Model.bulk(self,food_has_cat, False, 'Food_has_Categories',['FK_food_id', 'FK_categorie_id'])

            # Add foods shops
            if len(food_has_shop) > 0:
                Model.bulk(self, food_has_shop, False, 'Food_has_Shops', ['FK_food_id', 'FK_shop_id'])
        else:
            # Update Foods
            pass

    def __make_food_category(self, food):

        food_has_cat = []
        # Get Categories names
        if len(food.categories) > 0:
            cat_names = []
            for cat in food.categories:
                cat_names.append(cat.name)

            categories = list(food.categories)

            # check already exist
            if len(cat_names) > 0:
                food_id = (Food()).search_id(('uri =', food.uri))

                db_cat = (Category()).get_list(('name', 'PK_id'), ('name IN', cat_names))

                if len(db_cat) > 0:
                    for cat in db_cat:
                        name, id = cat
                        if name in cat_names:
                            obj = type('fhc', (object,), {})()
                            setattr(obj, 'FK_food_id', food_id)
                            setattr(obj, 'FK_categorie_id', id)
                            food_has_cat.append(obj)
                            cat_names.remove(name)
                            for category in categories:
                                if category.name == name:
                                    categories.remove(category)

                # if have name to create
                if len(cat_names) > 0:
                    (Category()).bulk(categories)
                    db_ids = (Category()).search_ids(('name IN', cat_names))
                    for id in db_ids:
                        obj = type('fhc', (object,), {})()
                        setattr(obj, 'FK_food_id', food_id)
                        setattr(obj, 'FK_categorie_id', id)

                        food_has_cat.append(obj)


        return food_has_cat

    def __make_food_shop(self, food):

        food_has_shop = []
        # Get Shops names
        if len(food.shops) > 0:
            shop_names = []
            for shop in food.shops:
                shop_names.append(shop.name)

            shops = list(food.shops)

            # check already exist
            if len(shop_names) > 0:
                food_id = (Food()).search_id(('uri =', food.uri))

                db_shop = (Shop()).get_list(('name', 'PK_id'), ('name IN', shop_names))

                if len(db_shop) > 0:
                    for shop in db_shop:
                        name, id = shop
                        if name in shop_names:
                            obj = type('fhs', (object,), {})()
                            setattr(obj, 'FK_food_id', food_id)
                            setattr(obj, 'FK_shop_id', id)
                            food_has_shop.append(obj)
                            shop_names.remove(name)
                            for sh in shops:
                                if sh.name == name:
                                    shops.remove(sh)

                # if have name to create
                if len(shop_names) > 0:
                    (Shop()).bulk(shops)
                    db_ids = (Shop()).search_ids(('name IN', shop_names))
                    for id in db_ids:
                        obj = type('fhs', (object,), {})()
                        setattr(obj, 'FK_food_id', food_id)
                        setattr(obj, 'FK_shop_id', id)
                        food_has_shop.append(obj)

        return food_has_shop
    @property
    def _get_name(self):
        """ property return object attribute name"""
        return self.name