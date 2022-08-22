import tkinter as tk
from GUI.Menu.CPPsubmenu import cppSubmenu
from GUI.Menu.Matriky_submenu import matrikaSubmenu
from GUI.Menu.narozeniny import narozeninySubmenu
from GUI.Menu.liturgicke_texty import texty

class MenuBar(tk.Menu):
    def __init__(self, parent, main_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main = main_frame
        matrikaSubmenu(self)
        cppSubmenu(self, self.main)
        narozeninySubmenu(self,self.main)
        texty (self,self.main)
        print(self.main)

        self.add_separator()



