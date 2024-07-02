import psutil
import os
import time

def GetPid():
    for proc in psutil.process_iter():
        print(proc)
        if (proc.name() == "vServer"):
            return proc.pid
    return -1

if os.geteuid() != 0:
    print("SUPE")
    os.system("sudo su")
if (__name__ == "__main__"):
    while True == True:
        if (GetPid() == -1):
            print("FAFAFA")
            os.system("./Velneo-vServer/vServer.sh -s")
        time.sleep(5)

