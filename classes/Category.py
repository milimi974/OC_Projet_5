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
        'name'
    ]

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__(args)



