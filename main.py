#!/_env/bin/python
# coding: utf-8

# load dependencies
# Import classes packages
from classes.User import User
from classes.Food import Food
from classes.Functions import *

# Import modules
import csv  # Manage cvs file
import urllib.request   # For download cvs file from http://
import datetime


class Main:
    """ Main class manage Application """

    # Class attributes
    config = {
        'max_entries': 250,
        'csv_uri': 'http://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'
    }

    def __init__(self):
        """ Constructor initialize module """
        # percent update value
        self.percent = 0.0
        self.entry_count = 0


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

            # Max line for one request
            max_req = self.config['max_entries']
            self.entry_count = reader.line_num
            percent = float(self.entry_count / max_req)
            # Start loop to read each line
            for row in reader:
                # Create a list of food object for each line
                if row['product_name']:
                    csv_foods.append(Main.__make_food(row))
                # If reach max line to read
                # Save or update
                if len(csv_foods) >= max_req:
                    Main.__create_foods(csv_foods)
                    # Rest food list
                    csv_foods = []
                    self.percent += percent
                    print("Mise à jour à {}%".format(self.percent))
                    break

            # Create last data
            print('------- Last Save -----')
            if len(csv_foods) > 0:
                Main.__create_foods(csv_foods)
            print("Mise à jour à 100%")

    @staticmethod
    def __create_foods(foods):
        """ Method create bulk food

        Keyword arguments:
        foods -- list of food object

        """

        # Get foods from db with food list name
        codes = []
        for el in foods:
            # Add name of food into the list for search in db
            codes.append(el.code)

        db_data = (Food()).search_by(('code IN', codes))

        # Compare Db_Food with Csv_Food
        add_list = []
        if db_data:
            print('Data found')
            for food in foods:
                found = False
                for db_food in db_data:
                    if food.code == db_food.code:
                        # If exist compare for update
                        print('Exist')
                        Main.__compare(food, db_food)
                        found = True
                        break
                # If new add to list for save
                if not found:
                    print('Create')
                    add_list.append(food)
        else:
            print('No data found')
            add_list = foods

        # save all new data
        if add_list:
            (Food()).bulk(add_list, False)

    @staticmethod
    def __compare(food, db_food):
        """ Method compare 2 food object """

        # If modified date different update
        if not str(food.modified) == str(db_food.modified):
            print("{} : {} -- {}".format("Modified", food.modified, db_food.modified))
            food.PK_id = db_food.PK_id
            # Update food
            food.save()
            # Update food categories
            food.update_categories(db_food)
            # Update food shops
            food.update_shops(db_food)
            print('Update ' + food.name)

    @staticmethod
    def __make_food(row):
        """ Method create an object food

        Keyword arguments:
        row -- list of food fields value

        """
        # Make time to database format
        created = datetime.datetime.fromtimestamp(
                int(row['created_t'])
            ).strftime('%Y-%m-%d %H:%M:%S')
        updated = datetime.datetime.fromtimestamp(
            int(row['last_modified_t'])
        ).strftime('%Y-%m-%d %H:%M:%S')

        # Arguments for instantiate Food
        args = {
            'PK_id': 0,
            'code': row['code'],
            'link': row['url'],
            'name': row['product_name'],
            'uri': row['product_name'],
            'description': row['ingredients_text'],
            'level': row['nutrition_grade_fr'],
            'created': created,
            'modified': updated,
            'shops': row['stores'],
            'categories': row['categories_fr'],
        }
        return Food(args)

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
        """
        args = {
            'fields': 'all',
            'where': [
                ('name LIKE', '%a%'),
            ],
            'limit': [0,20],

        }
        rep = (Food()).search_by(('name LIKE','%a%'))
        print(rep)
        """


    def test(self):

        csv_foods = []

        args = {
            'PK_id': 0,
            'code': '0000066655',
            'link': 'http://www.yoso.fr',
            'name': "Moutarde à l'Ancienne",
            'uri': "Moutarde à l'Ancienne",
            'description': "Les ingrédients sont listés par ordre d'importance (quantité)."
                           "Liste des ingrédients : Eau, graines de moutarde, vinaigre d'alcool,"
                           "sel, vin blanc (contient sulfites), sucre, épices, acidifiant : "
                           "acide citrique, conservateur : disulfite de potassium."
                           "Substances ou produits provoquant des allergies ou intolérances : "
                           "Moutarde, Anhydride sulfureux et sulfites",
            'level': 'a',
            'created': "2017-11-05 14:45:20",
            'modified': "2017-11-05 14:45:20",
            'shops': "Grand Frais,Auchan",
            'categories': "Epicerie,Condiments,Sauces,Moutardes,Moutardes à l'ancienne",
        }

        csv_foods.append(Food(args))
        args = {
            'PK_id': 0,
            'code': '0000066656',
            'link': 'http://www.yoso.fr',
            'name': "Mousse Au Café - Nova - 216 g (4 * 54 g)",
            'uri': "Mousse Au Café - Nova - 216 g (4 * 54 g)",
            'description': "Les ingrédients sont listés par ordre d'importance (quantité)."
                           "Liste des ingrédients : Eau, graines de moutarde, vinaigre d'alcool,"
                           "sel, vin blanc (contient sulfites), sucre, épices, acidifiant : "
                           "acide citrique, conservateur : disulfite de potassium."
                           "Substances ou produits provoquant des allergies ou intolérances : "
                           "Moutarde, Anhydride sulfureux et sulfites",
            'level': 'b',
            'created': "2017-11-05 14:45:20",
            'modified': "2017-11-05 14:45:20",
            'shops': "Grand Frais,Auchan,Leclerc",
            'categories': "Epicerie,Condiments,Sauces,Moutardes,Mousses lactées,Mousses sucrées,Mousses au café",
        }

        csv_foods.append(Food(args))
        Main.__create_foods(csv_foods)



main = Main()
main.test()

