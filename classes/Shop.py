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
        'name'
    ]

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__(args)
