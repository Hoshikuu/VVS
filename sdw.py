import psutil
import os
import time
import threading
    

def GetPid():
    for proc in psutil.process_iter():
        if (proc.name() == "vServer"):
            return proc.pid
    print("Servidor no detectado/n Posiblemente no encendido")
    return -1

def CheckServerStatus():
    if (GetPid() == -1):
        print("Encendiendo Servidor")
        os.system("./Velneo-vServer/vServer.sh -s")

if (__name__ == "__main__"):
    print("Script Activado")
    while True == True:
        CheckServerStatus()
        time.sleep(5)

