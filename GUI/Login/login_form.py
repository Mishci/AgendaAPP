from tkinter import *
from LOGIC.login_form_entries_validation import login_validation
from LOGIC.registration_form_entries_validation import reg_validation
from LOGIC.excel_data_load import excel_data_load
from LOGIC.weather import Weather
from apscheduler.schedulers.background import BackgroundScheduler
from LOGIC.email_send import sendemail


class LoginForm(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(height=700, width=550, bg="#7bacc7")
        self.pack(pady=(20, 0))



        # ----------------------ENTRIES FORM / entries.frame----------------------------------------------------------
        # login label
        self.label = Label(self, text="Přihlašte se!", font=("Arial", 14), bg="#7bacc7")
        self.label.pack()

        #login labelFrame
        self.entries_frame = LabelFrame(self, text="Přihlašovací data", borderwidth = 5, height=200, width=500, padx=100, pady=10, bg="lightblue")
        self.entries_frame.pack()

        # entry fields inside the entries.frame > obec + password
        self.obec_label = Label(self.entries_frame, text="Název NO", padx=10, pady=10, bg="lightblue" )
        self.obec_label.grid(row=0, column=0)
        entry_obec_var = StringVar(self.entries_frame)
        self.obec_entry = Entry(self.entries_frame, textvariable=entry_obec_var)
        self.obec_entry.grid(row=0, column=1, columnspan=2)
        self.obec_entry.focus_set()

        self.password_label = Label(self.entries_frame, text="Heslo", padx=10, pady=10, bg="lightblue")
        self.password_label.grid(row=1, column=0)
        entry_password_var = StringVar(self.entries_frame)
        self.password = Entry(self.entries_frame, textvariable=entry_password_var)
        self.password.grid(row=1, column=1, columnspan=2)

        # submit button
        self.button = Button(self.entries_frame, text="Přihlásit se",
                             command=lambda: self.close_on_succesfull_login(root, entry_obec_var, entry_password_var))
        self.button.grid(row=3, column=2, columnspan=2, sticky=E)



        # --------------------------REGISTRATION FORM /entries_reg-frame----------------------------------------------
        # reg label
        self.reg_label = Label(self, text="Registrujte se!", font=("Arial", 14), bg="#7bacc7")
        self.reg_label.pack(pady = (30,0))

        # reg labelFrame
        self.entries_reg_frame = LabelFrame(self, text="Registrační data", borderwidth = 5, height=200, width=500, padx=100, pady = 20, bg="lightblue")
        self.entries_reg_frame.pack()

        # reg entry fields inside entries_reg_form > obed_reg + password_reg
        self.obec_reg_label = Label(self.entries_reg_frame, text="Název NO", padx=10, pady=10, bg="lightblue")
        self.obec_reg_label.grid(row=0, column=0)
        entry_reg_obec_var = StringVar(self.entries_reg_frame)
        self.obec_reg_entry = Entry(self.entries_reg_frame, textvariable=entry_reg_obec_var)
        self.obec_reg_entry.grid(row=0, column=1, columnspan=2)
        self.obec_reg_entry.focus_set()

        self.password_reg_label = Label(self.entries_reg_frame, text="Heslo", padx=10, pady=10, bg="lightblue")
        self.password_reg_label.grid(row=1, column=0)
        entry_password_reg_var = StringVar(self.entries_reg_frame)
        self.password_reg = Entry(self.entries_reg_frame, textvariable=entry_password_reg_var)
        self.password_reg.grid(row=1, column=1, columnspan=2)

        # submit registration button
        self.button = Button(self.entries_reg_frame, text="Registrovat se",
                             command=lambda: self.close_on_succesfull_registration( entry_reg_obec_var, entry_password_reg_var))
        self.button.grid(row=3, column=2, columnspan=2, sticky=E)



        # ------------------------ IMAGE ----------------------------------------------------------------
        self.image_ref = PhotoImage(file="C:/Users/Michal/PycharmProjects/agenda/logoresized.png.png")
        img_label = Canvas(self, width=200, height=200, highlightthickness=0)
        img_label.pack(pady=20)
        img_label.create_image(100, 100, image=self.image_ref)

        self.update_idletasks()

    def close_on_succesfull_login(self, root, entryVar, passwordVar):
        success = login_validation(entryVar, passwordVar)
        if success:
            self.parent.destroy()
            root.grab_release()
            root.attributes('-topmost', 'true')
            excel_data_load(entryVar, passwordVar)
            #TODO> weather widget function call API every hour
            weather_widget = Weather(root, city=entryVar.get())
            # weather_widget.pack(side="bottom", fill="both", expand=True)
            weather_widget.return_weather() #initializing // the first call when GUI created
            sched = BackgroundScheduler() #running as a separate thread
            sched.add_job(weather_widget.return_weather, "interval", seconds=5) #circular call of API every 1 hour

            sched.start()




    def close_on_succesfull_registration(self, obecReg, passwordReg):
        success = reg_validation(obecReg, passwordReg)
        if success:
            sendemail(obecReg, passwordReg)




