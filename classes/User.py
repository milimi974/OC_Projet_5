#!/usr/bin/env python
# coding: utf-8

# Import Packages classes -> Modules
from classes.Food import Food

# Import Model parent
from classes.Model import Model


class User(Model):
    """ Class associate to table Users """

    # Database table name
    table = 'Users'

    # Table column names
    fields = [
        'PK_id',
        'name',
        'lastname',
    ]

    # Format fields
    format_fields = {
        'PK_id': 'primary',
        'name': 'varchar',
        'lastname': 'varchar',
    }

    def __init__(self, args={}):
        # Instantiate Parent
        super().__init__()

    def find_user_food(self, user_id):
        """ return list of user food saved

        Method arguments:
        user_id -- int

        """
        args = {
            'where': [
                ('User_has_Foods.FK_user_id =', int(user_id))
            ],
            'on': [
                ('Foods.PK_id =', 'User_has_Foods.FK_food_id'),
            ]
        }
        # get foods
        foods = (Food()).findjoin('User_has_Foods', args)
        return {'next_page': 0, 'before_page': 0, 'current_page': 1, 'total': len(foods),
                'response': foods}