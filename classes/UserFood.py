#!/usr/bin/env python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.Food import Food

# Import Model parent
from classes.Model import Model


class UserFood(Model):
    """ Manage food database """

    # Database table name
    table = 'User_has_Foods'

    # Table column names
    fields = [
        'FK_user_id',
        'FK_food_id',
    ]

    # Format fields
    format_fields = {
        'FK_user_id': 'primary',
        'FK_food_id': 'primary',
    }

