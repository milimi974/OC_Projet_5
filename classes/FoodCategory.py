#!/usr/bin/env python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.Category import Category

# Import Model parent
from classes.Model import Model


class FoodCategory(Model):
    """ Manage food database """

    # Database table name
    table = 'Food_has_Categories'

    # Table column names
    fields = [
        'FK_food_id',
        'FK_categorie_id',
    ]

    def __init__(self, args={}):
        """ Initialized Food object

        Keyword arguments:
        args -- list of product fields value

        """
        # Instantiate Parent
        super().__init__(args)

    @classmethod
    def make_food_category(cls, food, food_id):
        """ Add categories to new food

        Keyword arguments:
        food -- object for one food
        food_id -- id of food created
        """

        # Get Categories names
        if len(food.categories) > 0:

            food_has_cat = []

            cat_names = food.get_categories_uri

            categories = list(food.categories)

            # check already exist
            if len(cat_names) > 0:

                # control in database if categories already exist
                db_cat = (Category()).get_list(('uri', 'PK_id'), ('uri IN', cat_names))

                # If categories exist
                if len(db_cat) > 0:
                    for cat in db_cat:
                        name, id = cat
                        if name in cat_names:
                            food_has_cat.append(FoodCategory({'FK_food_id': food_id, 'FK_categorie_id': id}))
                            cat_names.remove(name)
                            for category in categories:
                                if category.name == name:
                                    categories.remove(category)

                # if have name to create
                if len(cat_names) > 0:
                    (Category()).bulk(categories)
                    db_ids = (Category()).search_ids(('uri IN', cat_names))
                    for id in db_ids:
                        food_has_cat.append(FoodCategory({'FK_food_id': food_id, 'FK_categorie_id': id}))

            # Add foods categories
            if len(food_has_cat) > 0:
                cls.bulk(food_has_cat)

    def remove(self):
        """ Remove entry on database """
