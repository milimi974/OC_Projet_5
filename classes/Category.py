#!/usr/bin/env python3.5
# coding: utf-8

# Import Model parent
from classes.Model import Model


class Category(Model):
    """"""

    def __init__(self,name):
        # Instanciate Parent
        super().__init__()
        self.name = name


