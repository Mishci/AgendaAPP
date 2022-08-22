#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from tkinter import filedialog, messagebox
import os.path
from LOGIC.zip_file import zip_file
from LOGIC.strip_accent import strip_accents

import pandas as pd


def excel_data_load(entryVar, passwordVar):

    account = entryVar.get()
    password = passwordVar.get()
    print (account)
    print(password)

    #run only one time for the every user / when excel file to load chosen, get the data, convert, zip
    #on the other runs, skipp this whole part of this function by else: pass
    if not os.path.isfile(f"PERSONAL/{account}/excel_back_{account}.zip"):
        try:
            #getting stored address of a excel file to load and convert, chosen bz the user by regisration filedialog
            with open("excel_data_load_check.json", "r") as load_check:
                data = json.load(load_check)
                print (data)
                address = data[account]["file_address"]



                #reading and converting mechanism
                # 1.getting rid of pandas timestamp 00:00:00
                # 2.creating a personal folder for every user
                # 3.converting the loaded and read excel to other formats> csv, json
                # 4. zipping the converted files with a hash/salt password into the personal folder

                try:
                    with open(address, "r") as db:  # check if excel file was not deleted or moved. if not, proceed
                        db_data = pd.read_excel(address)
                        db_data["Nar."] = pd.to_datetime(db_data["Nar."], errors='coerce')  # timestamp get rid
                        db_data["Nar."] = db_data["Nar."].dt.date  # overwrite |Nar.] values with no timestamp

                        if not os.path.exists(f"PERSONAL/{strip_accents(account)}"): #check for personal data dir f.e. personal/Kyjov
                            os.mkdir(f"PERSONAL/{strip_accents(account)}")  # create a personal dir if not exists

                        #convert data to csv / needed because of time stamp manipulation
                        db_data.to_csv(f"PERSONAL/{strip_accents(account)}/Data_{strip_accents(account)}.csv", date_format='d%m%Y', index=False, header=True)
                        csv = pd.read_csv(f"PERSONAL/{strip_accents(account)}/Data_{strip_accents(account)}.csv")

                        # converting csv to excel
                        if not os.path.isfile(f"PERSONAL/{strip_accents(account)}/excel_back_{strip_accents(account)}.xlsx"):
                            csv.to_excel(f"PERSONAL/{strip_accents(account)}/excel_back_{strip_accents(account)}.xlsx", index=None, header=True)
                            # getting the stored password hash

                            #1. zipping the excel file and protect by the password given by the user at registration
                            #2. deleting unprotected files .csv and .xlsx
                            zip_file(f"PERSONAL/{strip_accents(account)}/excel_back_{strip_accents(account)}.xlsx", password)
                            zip_file(f"PERSONAL/{strip_accents(account)}/Data_{strip_accents(account)}.csv", password)




                        pd.options.display.max_columns = len(csv.columns) #console on success check

                        print(csv)
                        excel_found = True
                        return excel_found

                except FileNotFoundError:
                    messagebox.showerror(title="EXCEL SOUBOR NENALEZEN", message="Soubor byl smazán nebo přesunut!")
                    excel_found = False
                    return excel_found


        # case excel file was not yet chosen and therefore its address has not been stored in excel_check json
        # 1. provide the open dialog to the user to chose a valid excel file
        # 2. create an excel_check json file and dump the address into it valid fot he particular user
        # 3. use the recursion of this whole excel_data_load function to pass the tries and get the data loaded and converted
        except FileNotFoundError:
            file = filedialog.askopenfilename(initialdir="/", title="Vyberte excel soubor pro načtení dat!",
                                              filetypes=[("Excel file", "*.xlsx"), ("Excel file", "*.xls")])

            with open("excel_data_load_check.json", "w",  ) as load_check:
                check = {
                    account: {
                        "file_address": file
                    }
                }

                json.dump(check, load_check, indent=4)
                load_check.close()

            if os.path.exists("excel_data_load_check.json"):
                excel_data_load(entryVar, passwordVar)



        # delete all tracks of the address of the chosen excel file for loading
        # data si now stored in excel...zip with no need to reveal the address of an original file on the disk
        finally:
            if os.path.isfile(f"PERSONAL/{strip_accents(account)}/excel_back_{strip_accents(account)}.zip") & os.path.isfile("excel_data_load_check.json"):
                os.remove("excel_data_load_check.json") # TODO > personalize the address
                os.remove(f"PERSONAL/{strip_accents(account)}/Data_{strip_accents(account)}.csv")
                os.remove(f"PERSONAL/{strip_accents(account)}/excel_back_{strip_accents(account)}.xlsx")


    else:
        pass




