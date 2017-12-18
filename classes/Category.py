#!/usr/bin/env python3.5
# coding: utf-8


# Import Model parent
from classes.Model import Model


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

    # Format fields
    format_fields = {
        'PK_id': 'primary',
        'uri': 'serialized',
        'name': 'varchar',
    }

    def __init__(self, args={}):

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
                ('Categories.PK_id =', 'Food_has_Categories.FK_category_id'),
            ]
        }
        return self.findjoin('Food_has_Categories',args)

    def make_categories(self, categories):
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
            category_uri = []

            # for each category remove term en and pl
            for category in categories:
                if 'en:' not in category and 'pl:' not in category:
                    cat = Category({'name': category, 'uri': category})
                    response.append(cat)
                    category_uri.append(cat.uri)

            if category_uri:
                # get categories already exist
                db_categories = self.find({'where': [('uri IN', category_uri)]})

                # var contains clone category uri
                add_categories = list(category_uri)

                if db_categories:
                    for category in db_categories:

                        # if uri found in csv categories remove
                        if category.uri in add_categories:
                            add_categories.remove(category.uri)

                # list of categories to create
                if add_categories:
                    """ remove from list category object 
                    category to not create """
                    for category in list(response):
                        if category.uri not in add_categories:
                            response.remove(category)

                    if response:
                        self.bulk(response)
                        db_categories = self.find({'where': [('uri IN', category_uri)]})

                response = db_categories
        return response

    def remove_category(self):
        pass

    def get_name(self):
        """ property return object attribute name"""
        return self.name