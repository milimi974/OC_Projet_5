#!/usr/bin/env python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.Category import Category
from classes.Shop import Shop
from classes.FoodCategory import FoodCategory
from classes.FoodShop import FoodShop


# Import Model parent
from classes.Model import Model


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
    # Format fields
    format_fields = {
        'PK_id': 'primary',
        'code': 'varchar',
        'uri': 'serialized',
        'link': 'url',
        'name': 'text',
        'description': 'text',
        'level': 'varchar',
        'created': 'datetime',
        'modified': 'datetime',
    }

    def __init__(self, args={}):
        """ Initialized Food object

        Keyword arguments:
        args -- list of product fields value

        """
        # Instantiate Parent
        super().__init__(args)

        if args:
            # If instantiate with data from database
            if self.PK_id and self.PK_id > 0:
                # Get categories from db
                self.categories = (Category()).get_categories(self.PK_id)
                # Get shops from db
                self.shops = (Shop()).get_shops(self.PK_id)
            else:

                # init attributes
                if 'categories' in args:
                    # Grab categories form db
                    self.categories = (Category()).make_categories(args['categories'])
                if 'shops' in args:
                    # Grab shops from db
                    self.shops = (Shop()).make_shops(args['shops'])

    def bulk(self, data, update=False):
        """ Override parent method

        Keyword arguments:
        data -- list of product from csv
        update -- boolean use active update action
        names -- list contain uri foods name

        """
        # Call parent method
        Model.bulk(self,data, update)

        if not update:
            # after create food

            # Loop for each food data
            for food in data:
                # Get Id of food created
                food_id = (Food()).search_id(('code =', food.code))

                # List of food categories to create
                (FoodCategory()).make_food_category(food, food_id)

                # List of food Shops to create
                (FoodShop()).make_food_shop(food, food_id)

        else:
            # Update Foods
            pass

    def update_categories(self, db_food):
        """ Update food categories

        Keyword arguments:
        db_food -- Food data from database

        """

        # var contains new categories id
        add_categories_id = []
        # list of categories uri
        db_categories = list(db_food.get_categories_uri)

        if len(self.categories) > 0:

            # if new category create and stack category to removed
            for category in self.categories:
                # if category isn't in db_categories create
                if category.uri not in db_categories:
                    add_categories_id.append(category.save())
                else:
                    db_categories.remove(category.uri)

            # If have category in list after check remove from db
            if len(db_categories) > 0:
                for category in db_categories:
                    FoodCategory(FoodCategory(
                        {'FK_food_id': db_food.PK_id,
                         'FK_category_id': category.PK_id})
                    ).remove()

        else:
            # If food no more have categories remove
            if len(db_categories) > 0:
                for category in db_categories:
                    FoodCategory(FoodCategory(
                        {'FK_food_id': db_food.PK_id,
                         'FK_category_id': category.PK_id})
                    ).remove()

    @property
    def get_categories_uri(self):
        """ extract categories name formated """

        cat_names = []
        if len(self.categories) > 0:
            for cat in self.categories:
                cat_names.append(cat.uri)

        return cat_names

    @property
    def get_shops_uri(self):
        """ extract shops name formated """

        shop_names = []
        if len(self.shops) > 0:
            for shop in self.shops:
                shop_names.append(shop.uri)

        return shop_names

    @property
    def _get_name(self):
        """ property return object attribute name"""
        return self.name