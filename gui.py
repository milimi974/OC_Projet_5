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

        # var current food index
        self.aliment = None

        # Add element in windows
        self.category_list = None
        self.status_bar = None
        self.input_category = None
        self.product_list = None
        self.button_next_page = None
        self.button_before_page = None
        self.description_box = None
        self.button_save_food = None

        # construct window
        self.build_window()

    def run(self):
        """ Display windows """
        # Start event loop
        self.master.mainloop()

    def build_window(self):
        # main Paned
        main_paned = tk.PanedWindow(self.master, orient=tk.VERTICAL)

        # title
        title = tk.Label(main_paned, text='Open Food Facts', font='system 24 bold', bg="white")
        main_paned.add(title)

        # container
        container_paned = tk.PanedWindow(main_paned, orient=tk.HORIZONTAL)
        container_paned.pack(expand="yes")

        ## left container
        container_left = tk.PanedWindow(container_paned, orient=tk.VERTICAL)
        container_left.pack(expand="yes")
        self.build_left_element(container_left)
        container_paned.add(container_left)

        ## right container
        container_right = tk.PanedWindow(container_paned, orient=tk.VERTICAL)
        container_right.pack(expand="yes")
        self.build_right_element(container_right)
        container_paned.add(container_right)

        main_paned.add(container_paned)

        # status bar
        self.status_bar = tk.Label(main_paned, text='Waiting ...', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill='x')
        main_paned.add(self.status_bar)

        # Display
        main_paned.pack(fill="both", expand="yes")

    def build_left_element(self, container_paned):
        """ build element on left side """
        # Found User Food
        label_frame_my = tk.LabelFrame(container_paned, text="Afficher la sauvegarde", padx=15, pady=15)
        label_frame_my.pack(fill="both", expand="yes")
        button_my_foods = tk.Button(label_frame_my, text='Retrouver mes aliments substitués',
                                    command=self.display_my_food_list)
        button_my_foods.pack()
        container_paned.add(label_frame_my)

        # Search category
        label_frame_search = tk.LabelFrame(container_paned, text="Rechercher une catégorie", padx=15, pady=15)
        label_frame_search.pack(fill="both", expand="yes")
        self.input_category = tk.Entry(label_frame_search)
        self.input_category.pack(side=tk.LEFT)
        button_search_category = tk.Button(label_frame_search, text='rechercher',
                                           command=self.display_food_category)
        button_search_category.pack(side=tk.LEFT)
        container_paned.add(label_frame_search)

        # Categories list
        label_frame_category = tk.LabelFrame(container_paned, text="Liste de catégories", padx=15, pady=15)
        label_frame_category.pack(fill="both", expand="yes")

        self.category_list = tk.Listbox(label_frame_category, cursor="arrow")
        self.category_list.pack(fill="both", expand="yes")
        self.category_list.bind('<<ListboxSelect>>', self.bind_category_selected)
        container_paned.add(label_frame_category)

    def build_right_element(self, container_paned):
        """ build element in right side """
        # foods list
        label_frame_foods = tk.LabelFrame(container_paned, text="Liste des aliments d'une categorie", padx=15, pady=15)
        label_frame_foods.pack(fill="both", expand="yes")

        self.product_list = tk.Listbox(label_frame_foods)
        self.product_list.pack(fill="both", expand="yes")
        self.product_list.bind('<<ListboxSelect>>', self.bind_food_selected)
        self.button_before_page = tk.Button(label_frame_foods, text='Précedente',
                                            command=self.display_before_page)
        self.button_before_page.pack(side=tk.LEFT)
        self.button_next_page = tk.Button(label_frame_foods, text='Suivante',
                                          command=self.display_next_page)
        self.button_next_page.pack(side=tk.LEFT)

        container_paned.add(label_frame_foods)

        # description
        label_frame_description = tk.LabelFrame(container_paned, text="Aliment de substitution", padx=15, pady=15)
        label_frame_description.pack(fill="both", expand="yes")
        self.description_box = tk.Text(label_frame_description)
        self.description_box.pack(fill="both", expand="yes")
        self.button_save_food = tk.Button(label_frame_description, text='Sauvegarder',
                                          command=self.add_user_food)
        self.button_save_food.pack(side=tk.LEFT)
        container_paned.add(label_frame_description)

    def display_food_category(self):
        """ Display food menu selection """
        # Get category name insert by user
        category_name = str(self.input_category.get())
        self.reset_form()
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
            self.status_bar['text'] = ''

    def bind_category_selected(self, event):
        """ user select a category"""

        w = event.widget
        if w.curselection():
            self.status_bar['text'] = 'Recherche des aliments de la categorie'
            self.reset_form()
            self.current_category_idx = int(w.curselection()[0])
            self.display_category_food_list()
        else:
            self.current_category_idx = None

    def display_category_food_list(self, page=1):
        """ Display category food list

        Keyword arguments:
        page -- int

        """
        # Get category index selected by user

        if not self.current_category_idx == None:

            pk_id = self.category_ids[self.current_category_idx]
            if pk_id:
                # read all food for category
                self.food_data = self.food.find_by_category(pk_id, page);
                self.display_food_list()

    def display_food_list(self):
        """ Add food in list box"""
        if self.food_data:
            # clear food list
            self.product_list.delete(0, tk.END)
            # Add food in name list
            if self.food_data['response']:
                for food in self.food_data['response']:
                    self.product_list.insert(tk.END, str(food.name))
            # status bar message
            self.status_bar['text'] = 'Page : ' + str(self.food_data['current_page'])

    def display_my_food_list(self):
        """ Display user food list """
        self.food_data = (User()).find_user_food(1)
        self.display_food_list()

    def bind_food_selected(self, event):
        """ user select a category"""
        w = event.widget
        if w.curselection():
            self.status_bar['text'] = 'Recherche de l\'aliment de substitution'
            idx = int(w.curselection()[0])
            self.aliment = self.food_data['response'][idx]
            self.description_box.delete(1.0, tk.END)
            self.display_food_description()
        else:
            self.current_food_idx = None

    def display_food_description(self):
        """ Display the description of food selected """

        # A product selected

        if self.aliment:
            food = self.food.find_better_nutricode(self.aliment)
            self.description_box.insert(tk.END,
                                        "Aliment : {} \n".format(food.name))
            self.description_box.insert(tk.END,
                                        "Description : {} \n".format(str(food.description)))
            self.description_box.insert(tk.END,
                                        "Categorie(s) : {} \n".format(','.join(food.get_categories_name)))
            self.description_box.insert(tk.END,
                                        "Magasin(s) : {} \n".format(','.join(food.get_shops_name)))
            self.description_box.insert(tk.END,
                                        "lien : {}".format(food.link))
            self.status_bar['text'] = 'Affichage aliment de substitution : ' + str(food.name)


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
        if self.aliment:

            # if save doesn't exist
            args = {
                'FK_user_id': 1,
                'FK_food_id': self.aliment.PK_id
            }
            user_food = UserFood(args)
            # check if save exist
            exist = user_food.findone({'where':[('FK_user_id =', 1),('FK_food_id =', self.aliment.PK_id)]})
            if not exist:
                user_food.save()
                self.status_bar['text'] = 'Sauvegarde : ' + str(self.aliment.name)
            else:
                self.status_bar['text'] = 'Sauvegarde déjà existante.'

            self.aliment.name = None

    def update_data_base(self):
        """ update dat in database from Open data food """
        (Update()).update_db

    def reset_form(self):
        """ hide and empty element """
        self.product_list.delete(0, tk.END)
        self.description_box.delete(1.0, tk.END)
        self.aliment = None