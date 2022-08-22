# -*- coding: windows-1250-*-
import smtplib, ssl
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText


import os

def sendemail (userName, passwordName):
    name = userName.get()
    pwd = passwordName.get()
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "agendaFU2022@gmail.com"
    receiver_email = "michal.devecka@gmail.com"
    password = os.environ.get("AgendaFU")
    print (password)


    Body = 'P�i registraci va�� NO do aplikace  jste pro p��stup ke sv�mu ��tu zadali n�sledovn� data: \n N�zev NO: {nazevNO} \n Heslo: {heslo}'.format(nazevNO=name,heslo=pwd)

    msg = MIMEMultipart("alternative")
    msg['Content-Type'] = "text/html; charset=ISO-8859-2"
    msg["Subject"] = "P�ihla�ovac� data do aplikace Agenda F�"
    msg["From"] = sender_email
    msg['To'] = ", ".join(receiver_email)

    message = MIMEText(Body, 'plain')
    msg.attach(message)  # attaching the text body into msg

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        print ("Nav�z�no spojen� so serverem")
        server.ehlo()  # Can be omitted
        server.starttls(context = context)
        print ("server podporuje starttls")
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        print("loginned to server")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("mail sent")




