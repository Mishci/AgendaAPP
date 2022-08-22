#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import pyminizip



def zip_file(fileName, password):
    # input file path
    inpt = fileName.encode("ISO 8859-2", errors="xmlcharrefreplace")
    inpt = inpt.decode("ISO 8859-2")

    # prefix path
    pre = None

    # output zip file path
    split = fileName.split(".")
    oupt = split[0]+(".zip")

    # set password value
    password = password.encode("ISO 8859-2", errors="xmlcharrefreplace")


    # compress level
    com_lvl = 5

    # compressing file
    print (f"password is: {password} ")
    password = password.decode ("ISO 8859-2")
    print(f"password is: {password} ")
    pyminizip.compress(inpt, None, oupt, password, com_lvl)



def unzip_file(fileName, password):

    with zipfile.ZipFile(fileName.join("zip")) as file:
        extracted = file.extractall(pwd=password.encode("ISO 8859-2", errors="xmlcharrefreplace"))
        return extracted
