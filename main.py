#!/_env/bin/python
# coding: utf-8


# Import Packages -> Modules
import tkinter as tk

# Import Project -> Modules
from gui import Gui

if __name__ == '__main__':
    root = tk.Tk()
    app = Gui(root)
    app.run()
    #app.update_data_base()