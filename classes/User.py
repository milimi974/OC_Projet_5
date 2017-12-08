#!/usr/bin/env python
# coding: utf-8

# Import Model parent
from classes.Model import Model


class User(Model):
    """ Class associate to table Users """

    # Database table name
    table = 'Users'

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__()
