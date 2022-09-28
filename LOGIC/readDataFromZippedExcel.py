#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zipfile import ZipFile
import pandas as pd
from LOGIC.strip_accent import strip_accents


def readDataFromZippedExcel():
    """"Tato funkce načítá data z heslem chráněného souboru, který byl vytvořen při registraci z excelového
    souboru vybraného uživatelem, encoduje čeká písmena a resetuje indexy"""
    from LOGIC.login_form_entries_validation import userGlobal
    from LOGIC.login_form_entries_validation import hesloGlobal

    # is not None only when login validation passed succesfully
    if hesloGlobal is not None and userGlobal is not None:
        print(userGlobal)
        print(hesloGlobal)
        try:
            with ZipFile(f"PERSONAL/{strip_accents(userGlobal)}/excel_back_{strip_accents(userGlobal)}.zip",
                         mode="r") as zip:
                with zip.open(f"excel_back_{strip_accents(userGlobal)}.xlsx", mode="r",
                              pwd=hesloGlobal.encode(encoding="utf-8", errors="xmlcharrefreplace")) as db:
                    data = pd.read_excel(db)
                    data.reset_index()

                    return data

        except FileNotFoundError:
            print("Soubor byl omylem smazan nebo presunut. Vytvorte si novy ucet a nahrajte nova data!")