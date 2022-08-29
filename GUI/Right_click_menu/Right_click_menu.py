#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Menu, LEFT



class RighClickMenu (Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.add_items()




    def add_items (self):
        self.add_command(label ="Edituj", compound=LEFT, command= self.edit)
        self.add_command(label ="Vymaž", compound=LEFT, command= self.delete_item)
        self.add_separator()

    def edit (self):
        print ("edituji")

    def delete_item (self):
        print("vymaži")

    def showMenu (self, event):
        try:
            from GUI.Menu.CPPsubmenu import y_coord, iid
            if y_coord > 0 :
                self.post(event.x_root, y_coord)
                print (y_coord)

        finally:
            self.grab_release()

