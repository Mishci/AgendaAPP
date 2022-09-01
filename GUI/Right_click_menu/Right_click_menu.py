#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Menu, LEFT
from GUI.Right_click_menu.Edit_pane import Edit_Pane


class RighClickMenu(Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.tree = master

        self.add_items()

    def add_items(self):
        self.add_command(label="Edituj", compound=LEFT, command=self.edit)
        self.add_command(label="Vymaž", compound=LEFT, command=self.delete_item)
        self.add_separator()

    def edit(self):
        from GUI.Menu.CPPsubmenu import iid
        data = self.tree.item (iid, "values")
        print(f"data {data}")
        columns = self.tree["columns"]
        print(f"columns = {columns}")
        output = tuple([(column,data[columns.index(column)]) for column in columns ])
        print(f"output = {output}" )
        Edit_pane_toplevel = Edit_Pane( column_data_tuples_list=output )

    def delete_item(self):
        print("Vymaž!")

    def showMenu(self, event):
        try:
            from GUI.Menu.CPPsubmenu import y_coord, iid
            if y_coord > 0 and iid is not None:
                self.post(event.x_root, y_coord)
                print(y_coord)

        finally:
            self.grab_release()

