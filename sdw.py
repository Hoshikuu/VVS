import psutil
import os
import time
import threading

def CountHalfHour():
    global timesStoped
    global counter
    localCounter = 0
    while counter == True:
        localCounter += 1
        time.sleep(1)
        if (localCounter == 30):
            timesStoped = 0
            localCounter = 0
            break
        print(localCounter)

def GetPid():
    for proc in psutil.process_iter(): 
        if (proc.name() == "vServer"):
            return proc.pid
    print("Servidor no detectado/n Posiblemente no encendido")
    return -1

def CheckServerStatus():
    global timesStoped
    global check
    global counter
    global tCount
    while check == True:
        if (GetPid() == -1):
            if (timesStoped == 0):
                tCount = threading.Thread(target=CountHalfHour)
                counter = True
                tCount.start()
            if (timesStoped == 3):
                print("El servidor se ha parado demasiadas veces, Deteniendo")
                check = False
                counter = False
                timesStoped = 0
                break
            timesStoped = timesStoped + 1
            print("Encendiendo Servidor")
            os.system("sudo sh Velneo-vServer/vServer.sh -s")
        time.sleep(5)

if (__name__ == "__main__"):
    print("Script Activado")
    timesStoped = 0
    counter = False
    check = False
    
    tCheck = threading.Thread(target=CheckServerStatus)
    tCount = threading.Thread(target=CountHalfHour)

    check = True
    tCheck.start()

    tCheck.join()
    tCount.join()
