from tkinter import ttk
from GUI.Menu.SearchPane.searchbox import searchComboBox

class SeachNFilterPannel(ttk.Combobox):
    def __init__(self, master, *args, **kwargs):
        ttk.Combobox.__init__(self, *args, **kwargs)
        searchComboBox(master)