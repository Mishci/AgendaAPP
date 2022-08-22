#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os

def pass_encrypt (psword):
    salt = os.urandom(32) # Remember this
    password = psword

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('ISO 8859-2', errors="xmlcharrefreplace"), # Convert the password to bytes
        salt, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128 # Get a 128 byte key
    )

    key.decode('ISO 8859-2', errors="xmlcharrefreplace")
    salt.decode('ISO 8859-2', errors="xmlcharrefreplace")
    return salt, key

def pass_verify (inputPsw, obec, data):
    salt = data[obec]["salt"]
    salt = salt.encode('ISO 8859-2', errors="xmlcharrefreplace")

    key_to_check = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        inputPsw.encode('ISO 8859-2', errors="xmlcharrefreplace"), # Convert the password to bytes
        salt, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128 # Get a 128 byte key
    )

    key_to_check = key_to_check.decode('ISO 8859-2', errors="xmlcharrefreplace")
    return key_to_check
