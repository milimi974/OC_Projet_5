#!/_env/bin/python3.5
# coding: utf-8

# Import Packages classes -> Modules
from classes.User import User
from classes.Food import Food
from classes.Food import Category

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
        self.food_ids = []

        # Add element in windows
        self._build_windows_elements()


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
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

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
        self.product_list = tk.Listbox(left_frame)
        button_category_foods = tk.Button(left_frame, text='Afficher les aliments',
                                    command=self.display_category_food_list)

        # Position elements
        button_my_foods.pack()
        label_category.pack()
        self.input_category.pack()
        button_search_category.pack()
        label_category_list.pack()
        self.category_list.pack()
        button_category_foods.pack()
        self.product_list.pack()

        # Defined status bar
        self.status_bar = tk.Label(bottom_frame, text='Waiting ...', bd=1, relief=tk.SUNKEN, anchor=tk.W)

        # Display status bar
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def display_food_category(self):
        """ Display food menu selection """
        # Get category name insert by user
        category_name = str(self.input_category.get())
        if category_name:
            # status bar message
            self.status_bar['text'] = 'Answering database ...'
            # get categories from database
            categories = self.category.get_list(('PK_id','name'),('name LIKE','%{}%'.format(category_name)))
            # clear category list
            self.category_list.delete(0, tk.END)
            # clear category ids list
            self.category_ids = []
            # Display all category
            for category in categories:
                pk_id, name = category
                self.category_list.insert(tk.END, name)
                self.category_ids.append(pk_id)
            # status bar message
            self.status_bar['text'] = 'Done ...'

    def display_category_food_list(self):
        """ Display category food list """
        # Get category index selected by user
        idx = self.category_list.curselection()[0]
        pk_id = self.category_ids[idx]
        if pk_id:
            # status bar message
            self.status_bar['text'] = 'Answering database ...'
            print(pk_id)
            # status bar message
            self.status_bar['text'] = 'Done ...'

    def display_my_food_list(self):
        """ Display user food list """
        print('Aficher ma list d\'aliment')
