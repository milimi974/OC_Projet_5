#!/usr/bin/env python
# coding: utf-8

# load dependences
# Import classes packages
import classes

class Main:
    """ Main class manage Application """

    def __init__(self, name, lastname):
        self.db = classes.Database()

    def run(self):
        print("That Run")

main = Main("yohan","solon")
main.run()