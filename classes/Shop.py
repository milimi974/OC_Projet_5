#!/usr/bin/env python
# coding: utf-8

# Import Model parent
from classes.Model import Model


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

    # Format fields
    format_fields = {
        'PK_id': 'primary',
        'uri': 'serialized',
        'name': 'varchar',
    }

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__(args)

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

    def make_shops(self,shops):
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

            # Format categories name
            shop_uri = []

            # for each shop remove term en and pl
            for shop in shops:
                shop_obj = Shop({'name': shop, 'uri': shop})
                response.append(shop_obj)
                shop_uri.append(shop_obj.uri)

            if shop_uri:
                # get categories already exist
                db_shops = self.find({'where': [('uri IN', shop_uri)]})

                # var contains clone shop uri
                add_shops = list(shop_uri)

                if db_shops:
                    for shop in db_shops:
                        if shop.uri in shop_uri:
                            add_shops.remove(shop.uri)

                # list of shops to create
                if add_shops:
                    for shop in list(response):
                        if shop.uri not in add_shops:
                            response.remove(shop)

                    if len(response) > 0:
                        self.bulk(response)
                        db_shops = self.find({'where': [('uri IN', shop_uri)]})

                response = db_shops
        return response

