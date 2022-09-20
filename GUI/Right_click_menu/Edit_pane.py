from tkinter import Toplevel, LabelFrame, Label, StringVar, PhotoImage
from GUI.Menu.Edit_item.Entry_with_placeholder import EntryWithPlaceholder



class Edit_Pane(Toplevel):
    def __init__(self, column_data_tuples_list, *args, **kwargs):
        Toplevel.__init__(self)
        self.geometry("630x450")
        self.config(bg="#7bacc7")
        self.title('  EDITUJ ZÁZNAM  ')
        self.iconphoto(True, PhotoImage(file="img.png"))
        self.attributes('-topmost', 'true')
        self.data_tuple_list = column_data_tuples_list
        # column name lists constants
        self.create_layout()



        # disabling the X-closing button
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.disable_close_on_X)

    def create_layout(self):
        # OSOBNI UDAJE LABELFRAME
        Basic_data_LFrame = LabelFrame(self, text="Osobní údaje", relief="sunken", height=200, width=580,
                                       highlightcolor="LightSeaGreen", bg="lightblue", bd=3, highlightthickness=5, font=("Arial", 12, "bold"), foreground = "red")
        Basic_data_LFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=15, )

        for i in range (0,3,2):

                # left label + entry
                Name_Label = Label(Basic_data_LFrame, text=self.data_tuple_list[i][0] + ":", bg="lightblue")
                Entry_name = EntryWithPlaceholder(Basic_data_LFrame, self.data_tuple_list[i][1])
                Name_Label.grid(column=0, row=i, padx=(20,10), pady=5)
                Entry_name.grid(column=1, row=i, padx=(20, 40), pady=5)

                if i+1 < 4:
                    # right label + entry
                    Surname_Label = Label(Basic_data_LFrame, text=self.data_tuple_list[i+1][0] + ":", bg="lightblue")
                    Entry_surname = EntryWithPlaceholder(Basic_data_LFrame, self.data_tuple_list[i+1][1])
                    Surname_Label.grid(column=2, row=i, padx=20, pady=5)
                    Entry_surname.grid(column=3, row=i, padx=(0, 20), pady=5)

        # DATUMY LABELFRAME
        Datumy_data_LFrame = LabelFrame(self, text="Datumy", relief="sunken", height=300, width=200,
                                       highlightcolor="LightSeaGreen", bg="lightblue", bd=3, highlightthickness=5,
                                       font=("Arial", 12, "bold"), foreground="red")
        Datumy_data_LFrame.grid(row=1, column=0, columnspan=1, padx=(20, 5), pady=15, sticky="n")

        index = 0
        for item in self.data_tuple_list[5:9]:
            Name_Label = Label(Datumy_data_LFrame, text=item[0] + ":", bg="lightblue")
            Entry_name = EntryWithPlaceholder(Datumy_data_LFrame, item[1])
            Name_Label.grid(column=0, row=index, padx=(20, 10), pady=5)
            Entry_name.grid(column=1, row=index, padx=(20, 40), pady=5)

            index += 1

        # CPP LABELFRAME
        CP_data_LFrame = LabelFrame(self, text="Církevní příspěvky", relief="sunken", height=300, width=200,
                                        highlightcolor="LightSeaGreen", bg="lightblue", bd=3, highlightthickness=5,
                                        font=("Arial", 12, "bold"), foreground="red")
        CP_data_LFrame.grid(row=1, column=1, columnspan=1, pady=15, padx=(0,20))

        index = 0
        for item in self.data_tuple_list[10:]:
            Name_Label = Label(CP_data_LFrame, text=item[0] + ":", bg="lightblue")
            Entry_name = EntryWithPlaceholder(CP_data_LFrame, item[1])
            Name_Label.grid(column=0, row=index, padx=(20, 10), pady=5)
            Entry_name.grid(column=1, row=index, padx=(20, 40), pady=5)

            index += 1

    def disable_close_on_X(self):
        self.destroy()
