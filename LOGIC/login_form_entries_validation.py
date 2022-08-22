import json
from tkinter import messagebox
from LOGIC.password_encrypt import pass_verify
import os.path

hesloGlobal = None # global var for sharing the inputted password to the main window to open / read zipped files
userGlobal = None

def login_validation (entryVar, passwordVar):
    obec = entryVar.get ()
    password = passwordVar.get()

    if len(obec) == 0 or len(password) == 0:
        messagebox.showinfo(title = "Oops",  message="Zabudli jste vyplnit údaje o obci, nebo zadat heslo!" )

    else:
        if os.path.isfile("personal_data.json"):
            with open("personal_data.json", "r") as data_file:
                data = json.load(data_file)


                if obec in data:
                    encrypted_password_input = pass_verify(password, obec, data)
                    print(encrypted_password_input)
                    if obec == data[obec]["obec"] and encrypted_password_input == data [obec]["password"]:
                        messagebox.showinfo(title="Úspěšné přihlášení", message="Vitejte ve svém účtu!")
                        success = True
                        # updating the global variable used in main app window to open zipped files
                        global hesloGlobal
                        hesloGlobal = password
                        global userGlobal
                        userGlobal = obec
                        return success
                    else:
                        messagebox.showerror(title="Neúpěšné přihlášení", message="Zadali jste nesprávné helo!")
                        success = False
                        return success
                else:
                    messagebox.showinfo(title="Dáta nenalezena!", message="Zkuste se přihlásit znovu!")
                    success = False
                    return success

        else:
            if not os.path.isfile("personal_data.json"):
                messagebox.showinfo(title="Dáta nenalezena!", message="Vyplňte registraci a poté se přihlašte!")
                success = False
                return success





