#!/usr/bin/env python
# coding: utf-8

# load dependences
# Import classes packages
from classes.Database import Database as DB
from classes.User import User
from classes.Food import Food
from classes.Category import Category
from classes.Shop import Shop

class Main:
    """ Main class manage Application """

    def __init__(self, name, lastname):
        self.db = DB()
        self.db.dbname = "keskonmamu803"
        self.db.name = "keskonmamu803"
        self.db.passwd = "99Admin99"
        self.db.host = "keskonmamu803.mysql.db"

    def __set_module(self):
        pass

    def run(self):
        print("That Run")
        self.db.connect

main = Main("yohan","solon")
main.run()