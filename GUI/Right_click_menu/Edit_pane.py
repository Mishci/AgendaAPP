from tkinter import Toplevel, LabelFrame, Label, StringVar, PhotoImage
from GUI.Menu.Edit_item.Entry_with_placeholder import EntryWithPlaceholder



class Edit_Pane(Toplevel):
    def __init__(self, column_data_tuples_list, *args, **kwargs):
        Toplevel.__init__(self)
        self.geometry("600x450")
        self.config(bg="#7bacc7")
        self.title('  EDITUJ ZÁZNAM  ')
        self.iconphoto(True, PhotoImage(file="img.png"))
        self.attributes('-topmost', 'true')
        self.data_tuple_list = column_data_tuples_list
        self.create_layout()

        #column name lists constants
        self.personalCols = ["Jméno", "Přijmění","Adresa", ]

        # disabling the X-closing button
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.disable_close_on_X)

    def create_layout(self):
        Basic_data_LFrame = LabelFrame(self, text="Osobní údaje", relief="sunken", height=200, width=580,
                                       highlightcolor="LightSeaGreen", bg="lightblue", bd=3, highlightthickness=5, font=("Arial", 12, "bold"), foreground = "red")
        Basic_data_LFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=15, )
        # Přímění
        Name_Label = Label(Basic_data_LFrame, text=self.data_tuple_list[0][0] + ":", bg="lightblue")
        Entry_name = EntryWithPlaceholder(Basic_data_LFrame, self.data_tuple_list[0][1])
        Name_Label.grid(column=0, row=0, padx=(20,10), pady=15)
        Entry_name.grid(column=1, row=0, padx=(20, 40), pady=15)
        # Jméno
        Surname_Label = Label(Basic_data_LFrame, text=self.data_tuple_list[1][0] + ":", bg="lightblue")
        Entry_surname = EntryWithPlaceholder(Basic_data_LFrame, self.data_tuple_list[1][1])
        Surname_Label.grid(column=2, row=0, padx=20, pady=15, )
        Entry_surname.grid(column=3, row=0, padx=(0, 20), pady=15)

    def disable_close_on_X(self):
        self.destroy()
