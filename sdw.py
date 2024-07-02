import psutil
import os
import time

def GetPid():
    for proc in psutil.process_iter():
        if (proc.name() == "vServer"):
            return proc.pid
    return -1

def CheckServerStatus():
    if (GetPid() == -1):
        os.system("./Velneo-vServer/vServer.sh -s")

if (__name__ == "__main__"):
    while True == True:
        if os.geteuid() != 0:
            os.system("sudo su")
            CheckServerStatus()
        else:
            CheckServerStatus()
        time.sleep(5)
