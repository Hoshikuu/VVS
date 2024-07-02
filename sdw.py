import psutil
import os
import time

def GetPid():
    for proc in psutil.process_iter():
        if (proc.name() == "vServer"):
            return proc.pid
    return -1

if os.geteuid() != 0:
    os.system("sudo su")
    os.system("cd ~")
if (__name__ == "__main__"):
    while True == True:
        if (GetPid() == -1):
            os.system("cd Velneo-vServer")
            os.system("./vServer.sh -s")
            os.system("cd ~")
        time.sleep(5)
