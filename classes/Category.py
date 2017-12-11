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

        if 'name' in args:
            self.uri = serialized_title(args['name'])

        # Instantiate Parent
        super().__init__(args)

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

    @classmethod
    def __make_categories(cls, categories):
        """ Return a list of categories object

        Keyword arguments:
        cls -- instance of class category
        categories -- string of product categories

        """

        # responses var
        response = []
        # test type of value if string
        if type(categories) is str and categories:

            # Make a list with string
            categories = categories.split(',')

            # Format categories name
            categorie_uri = []

            # for each category remove term en and pl
            for category in categories:
                if 'en:' not in category and 'pl:' not in category:
                    response.append(Category({'name': category}))
                    categorie_uri.append(serialized_title(category))

            # get categories already exist
            db_categories = cls.find({'where':[('uri IN', categorie_uri)]})

            # var contains clone category uri
            add_categories = list(categorie_uri)

            if len(db_categories) > 0:
                for category in db_categories:
                    if category.uri in categorie_uri:
                        add_categories.remove(category.uri)

            # list of categories to create
            if len(add_categories) > 0:
                for category in response:
                    if category.uri not in add_categories:
                        response.remove(category)

                if len(response) > 0:
                    cls.bulk(response)
                    db_categories = cls.find({'where': [('uri IN', categorie_uri)]})

            response = db_categories
        return response

    def remove_category(self):
        pass

    @property
    def _get_name(self):
        """ property return object attribute name"""
        return self.name