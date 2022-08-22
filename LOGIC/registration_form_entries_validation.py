
import json
import os.path
from tkinter import messagebox
from LOGIC.password_encrypt import pass_encrypt


def reg_validation(obecRegVar, passwordRegVar):
    obec_reg = obecRegVar.get()
    password_reg = passwordRegVar.get()
    salt_and_key = pass_encrypt(password_reg)

    new_reg = {
        obec_reg: {
            "obec": obec_reg,
            "salt": salt_and_key[0].decode("ISO 8859-2", errors="xmlcharrefreplace"),
            "password": salt_and_key[1].decode("ISO 8859-2", errors="xmlcharrefreplace"),
        },
    }

    # empty fields check
    if len(obec_reg) == 0 or len(password_reg) == 0:
        messagebox.showerror(title="Oops",
                             message="Zabudli jste vyplnit údaje o obci, nebo zadat heslo v registračním formuláři!")

    else:

        if os.path.isfile("personal_data.json"):
            with open("personal_data.json", "r+") as data_file:
                data = json.load(data_file)
                if obec_reg in data:  # block checking if password or obec are not already used bz other user
                    obec_check = data[obec_reg]["obec"]
                    password_check = data[obec_reg]["password"]
                    if obec_reg == obec_check:
                        messagebox.showerror(title="Ooops",
                                             message=f"Název: {obec_reg} pro obec již patří k účtu registrovanému v databázi! "
                                                     f"\n Zadejte jiný název obce!  ")
                        success = False
                        return success

                    if password_reg == password_check:
                        messagebox.showerror(title="Ooops",
                                             message=f"Heslo: {password_reg} pro již patří k účtu registrovanému v databázi! "
                                                     f"\n Zadejte jiné heslo!")

                        success = False
                        return success


                elif obec_reg not in data:  # if file found and data is not used by other user, append  (dump) data to the end of file
                    messagebox.showinfo(title="Gratulujeme!",
                                        message=f"Proběhla úspěšná registrace \n Název obce: {obec_reg} \n Heslo: {password_reg}")
                    data.update(new_reg)
                    with open("personal_data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                        success = True

                    return success

        else:  # if file not found, create file and write data automatically
            with open("personal_data.json", "w") as data_file:
                json.dump(new_reg, data_file, indent=4)
                messagebox.showinfo(title="Gratulujeme!",
                                    message=f"Proběhla úspěšná registrace \n Název obce: {obec_reg} \n Heslo: {password_reg}")
                success = True

            return success
