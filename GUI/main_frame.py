import tkinter as tk






class Main_Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master = master
        # ---- setting up Main_frame geometry and add the main menu to the root frame
        self.config(padx=10,pady=10, bg="#7bacc7", width=600)



        #adding the searchbox

        # --- adding submenus to menubar
        self.pack(side="top", fill="both", expand=True)





