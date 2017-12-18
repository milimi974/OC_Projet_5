#!/_env/bin/python3.5
# coding: utf-8

# Import Packages classes -> Modules
from classes.User import User
from classes.Food import Food
from classes.Food import Category
from classes.UserFood import UserFood

# Import Project -> Modules
from update import Update

# Import Packages -> Modules
import tkinter as tk


class Gui(tk.Frame):
    """ Class manage gui inherit tk module frame """

    # Class attributes
    config = {
        'max_entries': 250,
        'csv_uri': 'http://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'
    }

    # windows title -- str
    title = "Pure Beurre"

    def __init__(self, master ):
        """ Class constructor
        Parameters:
        master -- object tkinter
        """
        super().__init__(master)

        # Add title -> windows
        self.master.title(self.title)

        # Set background color
        self.master['bg'] = 'white'

        # init Food object
        self.food = Food();

        # init User object
        self.user = User();

        # init Category object
        self.category = Category();

        # var categories
        self.category_ids = []

        # var foods
        self.food_data = []

        # var current category index
        self.current_category_idx = None

        # var current food index
        self.current_food_idx = None

        # Add element in windows
        self._build_windows_elements()

        # Hidden element
        self.button_next_page.pack_forget()
        self.button_before_page.pack_forget()
        self.button_description_food.pack_forget()
        self.button_save_food.pack_forget()

    def run(self):
        """ Display windows """
        # Start event loop
        self.master.mainloop()

    def _build_windows_elements(self):
        """ Add elements in windows """

        # defined Frame
        top_frame = tk.Frame(self.master, bg="white")
        bottom_frame = tk.Frame(self.master)

        # Display Frames
        top_frame.pack(fill=tk.X)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # defined container
        middle_container = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)

        # Display container
        middle_container.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=15, padx=15)

        # defined Frame
        left_frame = tk.Frame(middle_container)
        right_frame = tk.Frame(middle_container, bg="red")

        # Display frame
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Defined elements top frame
        tk.Label(top_frame, text='Open Food Facts', font='system 24 bold', bg="white").pack()

        # Defined elements left frame
        label_category = tk.Label(left_frame, text='Categorie')
        label_category_list = tk.Label(left_frame, text='Liste des categories')
        self.input_category = tk.Entry(left_frame)
        button_search_category = tk.Button(left_frame, text='valider', command=self.display_food_category)
        self.category_list = tk.Listbox(left_frame)
        button_my_foods = tk.Button(left_frame, text='Retrouver mes aliments substitués',
                                    command=self.display_my_food_list)
        button_category_foods = tk.Button(left_frame, text='Afficher les aliments',
                                          command=self.display_category_food_list)

        # Defined elements right frame
        self.product_list = tk.Listbox(right_frame)
        self.button_next_page = tk.Button(right_frame, text='Suivante',
                                          command=self.display_next_page)
        self.button_before_page = tk.Button(right_frame, text='Précedente',
                                            command=self.display_before_page)
        self.button_description_food = tk.Button(right_frame, text='Afficher la description',
                                            command=self.display_food_description)
        self.description_box = tk.Text(right_frame)
        self.button_save_food = tk.Button(right_frame, text='Sauvegarder',
                                          command=self.add_user_food)
        # Position elements
        button_my_foods.pack()
        label_category.pack()
        self.input_category.pack()
        button_search_category.pack()
        label_category_list.pack()
        self.category_list.pack()
        button_category_foods.pack()
        self.product_list.pack()
        self.button_next_page.pack()
        self.button_before_page.pack()
        self.button_description_food.pack()
        self.description_box.pack()
        self.button_save_food.pack()

        # Defined status bar
        self.status_bar = tk.Label(bottom_frame, text='Waiting ...', bd=1, relief=tk.SUNKEN, anchor=tk.W)

        # Display status bar
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def display_food_category(self):
        """ Display food menu selection """
        # Get category name insert by user
        category_name = str(self.input_category.get())
        # reset data
        self.reset_category()

        if category_name:
            # status bar message
            self.status_bar['text'] = 'Answering database ...'
            # get categories from database
            categories = self.category.get_list(('PK_id', 'name'), ('name LIKE', '%{}%'.format(category_name)))
            # clear category list
            self.category_list.delete(0, tk.END)
            # clear category ids list
            self.category_ids = []
            # display all category
            for category in categories:
                pk_id, name = category
                self.category_list.insert(tk.END, name)
                self.category_ids.append(pk_id)
            # status bar message
            self.status_bar['text'] = 'Done ...'

    def display_category_food_list(self, page=1):
        """ Display category food list

        Keyword arguments:
        page -- int

        """
        # Get category index selected by user

        if self.category_list.curselection():
            current_idx = self.category_list.curselection()[0]

            if self.current_category_idx != current_idx:
                self.current_category_idx = current_idx

            pk_id = self.category_ids[self.current_category_idx]
            if pk_id:
                # status bar message
                self.status_bar['text'] = 'Answering database ...'
                # read all food for category
                self.food_data = self.food.find_by_category(pk_id, page);
                self.display_food_list()
                self.button_description_food.pack()

    def display_food_list(self):
        """ Add food in list box"""
        if self.food_data:
            # clear food list
            self.product_list.delete(0, tk.END)
            # Add food in name list
            if self.food_data['response']:
                for food in self.food_data['response']:
                    self.product_list.insert(tk.END, str(food.name))
            # show before button
            if self.food_data['before_page'] > 0:
                self.button_before_page.pack()
            else:
                self.button_before_page.pack_forget()
            # show next button
            if self.food_data['next_page'] > 0:
                self.button_next_page.pack()
            else:
                self.button_next_page.pack_forget()
            # status bar message
            self.status_bar['text'] = 'Page :' + str(self.food_data['current_page'])

    def display_my_food_list(self):
        """ Display user food list """
        self.food_data = (User()).find_user_food(1)
        self.display_food_list()

    def display_food_description(self):
        """ Display the description of food selected """

        # A product selected

        if self.product_list.curselection():
            current_idx = self.product_list.curselection()[0]

            if self.current_food_idx != current_idx:
                self.current_food_idx = current_idx

            aliment = self.food_data['response'][self.current_food_idx]
            self.product_list.delete(0, tk.END)
            if aliment:
                food = self.food.find_better_nutricode(aliment)
                self.description_box.insert(tk.END,
                                            "Aliment : {} \n".format(food.name))
                self.description_box.insert(tk.END,
                                            "Description : {} \n".format(str(food.description)))
                self.description_box.insert(tk.END,
                                            "Categorie(s) : {} \n".format(','.join(food.get_categories_name)))
                self.description_box.insert(tk.END,
                                            "Magasin(s) : {} \n".format(','.join(food.get_shops_name)))
                self.description_box.insert(tk.END,
                                            "liens : {}".format(food.link))
                self.status_bar['text'] = 'Affichage aliment de substitution : ' + str(food.name)
                self.button_save_food.pack()

    def display_next_page(self):
        """ Display next page foods """
        if self.food_data['next_page']:
            self.display_category_food_list(self.food_data['next_page'])

    def display_before_page(self):
        """ Display before page foods """
        if self.food_data['before_page']:
            self.display_category_food_list(self.food_data['before_page'])

    def add_user_food(self):
        """ save user food selected """
        if self.current_food_idx:
            aliment = self.food_data['response'][self.current_food_idx]
            # if save doesn't exist
            args = {
                'FK_user_id': 1,
                'FK_food_id': aliment.PK_id
            }
            user_food = UserFood(args)
            # check if save exist
            exist = user_food.findone({'where':[('FK_user_id =', 1),('FK_food_id =', aliment.PK_id)]})
            if not exist:
                user_food.save()
                self.status_bar['text'] = 'Sauvegarde : ' + str(aliment.name)
            else:
                self.status_bar['text'] = 'Sauvegarde déjà existante.'
            self.button_save_food.pack_forget()

    def update_data_base(self):
        """ update dat in database from Open data food """
        (Update()).update_db

    def reset_description(self):
        """ hide element """
        self.product_list.delete(0, tk.END)
        self.description_box.delete(1.0, tk.END)
        self.button_save_food.pack_forget()
        self.button_description_food.pack_forget()
        self.current_food_idx = None

    def reset_category(self):
        """ hide element """
        self.category_list.delete(0, tk.END)
        self.button_before_page.pack_forget()
        self.button_next_page.pack_forget()
        self.current_category_idx = None
        self.reset_description()