#!/usr/bin/env python
# coding: utf-8

# load dependences
# Import classes packages
from classes.Database import Database as DB
from classes.User import User
from classes.Food import Food


class Main:
    """ Main class manage Application """

    def __init__(self):
        """ Constructor initialize module """

        # Create Database module
        self.db = DB()

        # Max insert or update request to DB
        self.max_req = 50

    def update_db(self):
        """ Public methode for updating database from csv"""


        # Read Csv file from url

        # Start loop to read each line

        # Create a list a food object for each line

        # Add name of food into the list for search in db

        # If reach max line to read

        # Get foods from db with food list name

        # Compare Db_Food with Csv_Food

        # If new add to list for save

        # If update add to list for update

        # Add new Foods

        # Update Foods

        # Reset max line to read

        pass
    def __set_module(self):
        pass

    def run(self):
        """ public methode start application"""

        print("That Run")


main = Main()
main.run()

class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
             cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1

    def result(self):
        return self.count

one = Singleton()
two = Singleton()

one.add()
two.add()
two.add()

print(one.count)
print(two.count)
print(one.count)