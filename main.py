#!/_env/bin/python3.5
# coding: utf-8

# load dependences
# Import classes packages
from classes.Database import Database as DB
from classes.User import User
from classes.Food import Food

# Import modules
import csv # Manage cvs file
import urllib.request # For download cvs file from http://

class Main:
    """ Main class manage Application """

    # Class attributes
    config = {
        'max_entries': 50,
        'csv_uri': 'http://world.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
    }

    def __init__(self):
        """ Constructor initialize module """

        # Create Database module
        self.db = DB()

    def update_db(self):
        """ Public methode for updating database from csv"""

        # vars
        new_food = []
        update_food = []

        # Read Csv file from url
        with open('./uploads/food.csv', newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:

                pass

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


    def __set_module(self):
        pass

    @property
    def upload_csv(self):
        """ That property simply download csv file source to local """

        urllib.request.urlretrieve(self.config['csv_uri'], './uploads/food.csv')

    @property
    def run(self):
        """ public methode start application"""

        self.update_db()
        print("That Run")


main = Main()
main.run