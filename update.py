#!/_env/bin/python
# coding: utf-8

# Import Packages classes -> Modules
from classes.User import User
from classes.Food import Food

# Import python -> Modules
import csv  # Manage cvs file
import urllib.request   # For download cvs file from http://
import datetime


class Update:
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
            # Start loop to read each line
            for row in reader:
                # Create a list of food object for each line
                if row['product_name']:
                    csv_foods.append(Update.__make_food(row))
                # If reach max line to read
                # Save or update
                if len(csv_foods) >= max_req:
                    Update.__create_foods(csv_foods)
                    # Rest food list
                    csv_foods = []

            # Create last data
            if len(csv_foods) > 0:
                Update.__create_foods(csv_foods)
            print('End _ update')

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
            for food in foods:
                found = False
                for db_food in db_data:
                    if food.code == db_food.code:
                        # If exist compare for update
                        Update.__compare(food, db_food)
                        found = True
                        break
                # If new add to list for save
                if not found:
                    add_list.append(food)
        else:
            add_list = foods

        # save all new data
        if add_list:
            (Food()).bulk(add_list, False)

    @staticmethod
    def __compare(food, db_food):
        """ Method compare 2 food object """

        # If modified date different update
        if not str(food.modified) == str(db_food.modified):
            food.PK_id = db_food.PK_id
            # Update food
            food.save()
            # Update food categories
            food.update_categories(db_food)
            # Update food shops
            food.update_shops(db_food)

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

    @property
    def upload_csv(self):
        """ That property simply download csv file source to local """
        urllib.request.urlretrieve(self.config['csv_uri'], './uploads/food.csv')


