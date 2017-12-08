#!/_env/bin/python3.5
# coding: utf-8

# load dependences
# Import classes packages
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
        'csv_uri': 'http://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'
    }

    def __init__(self):
        """ Constructor initialize module """



    @property
    def update_db(self):
        """ Public property for updating database from csv"""

        # vars
        new_food = []
        update_food = []
        csv_foods = []

        # Read Csv file from url
        with open('./uploads/food.csv', newline='', encoding='utf-8') as csvfile:
            # Associating header with value in a dictionary
            reader = csv.DictReader(csvfile, delimiter='\t')
            # Start loop to read each line

            max = self.config['max_entries']

            for row in reader:
                # Arguments for instanciate Food
                args = {
                    'PK_id': 0,
                    'code': row['code'],
                    'link': row['url'],
                    'name': row['product_name'],
                    'description': row['ingredients_text'],
                    'level': row['nutrition_grade_fr'],
                    'created': row['created_t'],
                    'modified': row['last_modified_t'],
                    'shops': row['stores'],
                    'categories': row['categories_fr'],
                }

                csv_foods.append(Food(args))
                # If max data to execute
                # Save or update
                if(len(csv_foods) >= max):
                    pass

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

        self.update_db
        print("That Run")


main = Main()
# main.run
print(main.__dict__)
