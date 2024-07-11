#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

from psutil import process_iter
from os import system
from time import sleep
from threading import Thread
from pushbullet import Pushbullet, InvalidKeyError
from configparser import ConfigParser
from colorama import init, Fore
from progress.bar import ChargingBar
from progress.spinner import Spinner
from datetime import datetime

def Clear():
    system("clear")

#---------------------------------------------------------------------------------------------


#*Barras de carga
#---------------------------------------------------------------------------------------------
def BarNext():
    bar.next()
    sleep(0.05)

def SpinNext():
    for i in range(10):
        spinner.next()
        sleep(0.1)
#---------------------------------------------------------------------------------------------


#*Contadores
#---------------------------------------------------------------------------------------------
#Contador del tiempo limite antes de que se reinicie el contador de cuantas veces se paro el server
def CountTime():
    global timesStoped, counter
    localCounter = 0
    
    while counter == True:
        localCounter += 1
        sleep(1)
        if (localCounter == counterLimit):
            timesStoped = 0
            localCounter = 0
            break
#---------------------------------------------------------------------------------------------


#Log
#---------------------------------------------------------------------------------------------
#Escribir log
def WriteLog(log):
    with open(f"./logs/log-{datetime.now().date()}.log", "a+") as file:
        file.write(f"[{datetime.now().strftime("%H:%M:%S")}]    " + log + "\n")
        file.close()
#---------------------------------------------------------------------------------------------


#*Procesos
#---------------------------------------------------------------------------------------------
#Obtener el identificador del proceso, si no se detecta manda una alerta
def GetPid():
    WriteLog("Identificando procesos")
    for proc in process_iter(): 
        if (proc.name() == processName):
            return proc.pid
    print("""
        Servidor no detectado
        Posiblemente no encendido
        """) #!
    WriteLog("Servidor no detectado")
    pushB.push_note("Atención: Servidor no detectado", stopText)
    return -1

#Bloque principal del programa, comprueba el estado del servidor cada cierto tiempo
def CheckServerStatus():
    WriteLog("Comprobando estado del servidor")
    global timesStoped, check, counter, tCount
    while check == True:
        sleep(checkPeriod)
        if (maintenance == True):
            WriteLog("En Mantenimiento, si esto no es lo esperado porfavor revise el archivo de configuracion")
            continue
        if (GetPid() != -1):
            WriteLog("Estado normal del servidor")
            continue
        WriteLog("Servidor Apagado")
        if (timesStoped == 0):
            WriteLog("Empezando contador")
            tCount = Thread(target=CountTime)
            counter = True
            tCount.start()
        if (timesStoped == stopLimit): #Parar a cierta cantidad, archivo config
            WriteLog("Servidor parado demasiadas veces, parando")
            WriteLog("Enviando notificacion")
            pushB.push_note("Precaución: Servidor no detectado", hardStopText)
            print("El servidor se ha parado demasiadas veces, Deteniendo") #!
            check = False
            counter = False
            timesStoped = 0
            sleep(3)
            break
        timesStoped = timesStoped + 1
        WriteLog(f"Encendiendo Servidor, veces parado: {timesStoped}")
        print("Encendiendo Servidor") #!
        system("sudo ../Velneo-vServer/vServer.sh -s") # Encender el servidor
#---------------------------------------------------------------------------------------------


#*Archivo de Configuracion
#---------------------------------------------------------------------------------------------
#Leer el archivo de configuracion
def ReadConfig(file, section, key): #Introducir el archivo de configuracion, se consigue con la funcion de ConfigConfig
    WriteLog(f"Leyendo configuracion de la seccion {section}, clave {key}")
    try:
        parser.read(file)
        datos = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                datos[param[0]] = param[1]
        else:
            raise TypeError
        return datos[key]
    except TypeError:
        WriteLog("ERROR     Seccion no se encuentra en el fichero")
        print(Fore.RED+f"Seccion {section} no se encuentra en el fichero {file}") #!
    except FileNotFoundError:
        WriteLog("ERROR     El fichero de configuracion no existe, probar eliminar el directorio de configuracion")
        print(Fore.RED+f"El fichero {file} no existe") #!

#Funcion absoluta para conseguir la ruta del archivo de configuracion, devuelve la ruta del archivo de configuracion
def ConfigConfig():
    file = "./Config/config.ini"
    section = "config"
    datos = ReadConfig(file, section, "config")
    return datos
#---------------------------------------------------------------------------------------------


#*Main
#---------------------------------------------------------------------------------------------
if (__name__ == "__main__"):
    init(autoreset=True)
    WriteLog("Programa iniciado")
    #Inicializacion inicial
    #----------------------------------------------------------------------------
    parser = ConfigParser()

    WriteLog("Cargando variables iniciales")
    bar = ChargingBar("Cargando variables iniciales", max=4)
    #Inicial VAR
    timesStoped = 0
    BarNext()
    counter = False
    BarNext()
    check = False
    BarNext()
    config = ConfigConfig()
    BarNext()
    bar.finish()

    WriteLog("Cargando variables importantes")
    bar = ChargingBar("Cargando variables importantes", max=9)
    #Important VAR
    processName = ReadConfig(config, "general", "processname")
    BarNext()
    counterLimit = int(ReadConfig(config, "time", "secondsreset"))
    BarNext()
    checkPeriod = int(ReadConfig(config, "time", "secondscheck"))
    BarNext()
    stopLimit = int(ReadConfig(config, "general", "stoplimit"))
    BarNext()
    apiKey = ReadConfig(config, "pushbullet", "apikey")
    BarNext()
    stopText = ReadConfig(config, "pushbullet", "stoptext")
    BarNext()
    hardStopText = ReadConfig(config, "pushbullet", "hardstoptext")
    BarNext()
    maintenanceT = ReadConfig(config, "general", "maintenance")
    BarNext()
    if (maintenanceT == "False" or maintenanceT == "false"):
        maintenance = False
    if (maintenanceT == "True" or maintenanceT == "true"):
        maintenance = True
    BarNext()
    bar.finish()

    spinner = Spinner("Conectando con PushBullet ")
    t1 = Thread(target=SpinNext)
    t1.start()
    #Conectar el PushBullet
    try:
        WriteLog("Conectando con pushbullet")
        pushB = Pushbullet(apiKey)
    except InvalidKeyError:
        WriteLog("Error     Conexion fallida con push bullet, probablemente token invalido")
        print("El token introducido no es valido, porfavor vuelva a ejecutar el programa")
        system("sudo rm -r -f ../Config")
        sleep(5)
        exit()
    WriteLog("Pushbullet iniciado correctamente")
    t1.join()
    spinner.finish()
    #----------------------------------------------------------------------------
    Clear()
    WriteLog("Todo iniciado correctamente, comenzando")
    print("Script Activado, pulsa 'Control + A + D' para salir de esta Pantalla")

    tCheck = Thread(target=CheckServerStatus)
    tCount = Thread(target=CountTime)

    check = True
    tCheck.start()

    tCheck.join()
    tCount.join()
#--------------------------------------------------------------------------------
