#!/usr/bin/env python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.Shop import Shop

# Import Model parent
from classes.Model import Model


class FoodShop(Model):
    """ Manage food database """

    # Database table name
    table = 'Food_has_Shops'

    # Table column names
    fields = [
        'FK_food_id',
        'FK_shop_id',
    ]
    # Format fields
    format_fields = {
        'FK_food_id': 'primary',
        'FK_shop_id': 'primary',
    }

    def __init__(self, args={}):
        """ Initialized Food object

        Keyword arguments:
        args -- list of product fields value

        """
        # Instantiate Parent
        super().__init__(args)

    def make_food_shop(self, food, food_id):
        """ Add shops to new food

        Keyword arguments:
        food -- object for one food
        food_id -- id of food created
        """

        # Get Shops names
        if len(food.shops) > 0:

            food_has_shop = []

            shop_names = food.get_shops_uri

            shops = list(food.shops)

            # check already exist
            if len(shop_names) > 0:

                db_shop = (Shop()).get_list(('uri', 'PK_id'), ('uri IN', shop_names))

                # If shops already exist
                if len(db_shop) > 0:
                    for shop in db_shop:
                        name, id = shop
                        if name in shop_names:
                            food_has_shop.append(FoodShop({'FK_food_id': food_id, 'FK_shop_id': id}))
                            shop_names.remove(name)
                            for sh in shops:
                                if sh.name == name:
                                    shops.remove(sh)

                # if have name to create
                if len(shop_names) > 0:
                    (Shop()).bulk(shops)
                    db_ids = (Shop()).search_ids(('uri IN', shop_names))
                    for id in db_ids:
                        food_has_shop.append(FoodShop({'FK_food_id': food_id, 'FK_shop_id': id}))

            # Add foods categories
            if len(food_has_shop) > 0:
                self.bulk(food_has_shop)