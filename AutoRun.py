#                                                                    ---------------------------------
#
#                                                                       Script  creado por  Hoshiku
#                                                                       https://github.com/Hoshikuu
#
#                                                                    ---------------------------------

from os import system, geteuid, listdir, mkdir, chmod
from os.path import exists, abspath, isfile
from time import sleep, time
from datetime import datetime
from sys import exit
from configparser import ConfigParser
from colorama import init, Fore
from progress.bar import Bar
from progress.spinner import Spinner

def Clear():
    system("clear")

#---------------------------------------------------------------------------------------------


#*Programa
#---------------------------------------------------------------------------------------------
#Empezar el programa principal
def StartProgram():
    system(f"sudo screen sudo {ReadConfig(config, "general", "bin")}/ServerStatusDetecter")
    Clear()
    WriteLog("Programa comenzado")
    print(Fore.BLUE+f"{round(time()-inicialTime, 4)}: Comenzado Correctamente") #!
#---------------------------------------------------------------------------------------------


#*Dependencias
#---------------------------------------------------------------------------------------------
#Comprobar que este instalado la dependencia "Screen" de linux
#Descargar si no esta descargado
def CheckDependencies():
    WriteLog("Comprobando dependecias")
    if (not exists(ReadConfig(config, "screens", "screenapt"))):
        WriteLog("No se encontro la dependencia necesaria")
        print(Fore.BLUE+"""
        Dependencias necesarias no encontradas
        Instalando
            """) #!
        sleep(2)
        try:
            WriteLog("Descargando dependencia 'screen'")
            system("sudo apt install screen")
            if (not exists(ReadConfig(config, "screens", "screenapt"))):
                WriteLog("No se completo la descarga de la dependencia")
                raise FileNotFoundError
            WriteLog("Se completo la descarga de la dependencia")
            print(f"{round(time()-inicialTime, 4)}: Dependencias instaladas correctamente") #!
        except FileNotFoundError:
            WriteLog("ERROR     No se completo la descarga de la dependencia")
            print(f"{round(time()-inicialTime, 4)}: No se completo la descarga de alguna manera, porfavor pruebe instalarlo manualmente con 'sudo apt install screen'") #!
            exit()
        except Exception:
            WriteLog("ERROR     No se completo la descarga de la dependencia")
            print(f"{round(time()-inicialTime, 4)}: No se pudo Descargar automaticamente, instale la dependencia con 'sudo apt install screen'") #!
            exit()

#Crear archivos necesarios para el archivo de configuracion
def CheckConfig():
    WriteLog("Comprobando configuracion")
    if (not exists("./Config")):
        WriteLog("Creando directorio de configuracion")
        mkdir("./Config")
        print(f"{round(time()-inicialTime, 4)}: Directorio de configuracion creado") #!

    if (not isfile("./Config/config.ini")):
        WriteLog("Creando fichero de configuracion")
        WriteConfig()
        print(f"{round(time()-inicialTime, 4)}: Fichero de configuracion generado") #!
#---------------------------------------------------------------------------------------------


#Log
#---------------------------------------------------------------------------------------------
#Escribir log
def WriteLog(log):
    with open(f"./logs/log-{datetime.now().date()}.log", "a+") as file:
        file.write(f"[{datetime.now().strftime("%H:%M:%S")}]    " + log + "\n")
        file.close()
#---------------------------------------------------------------------------------------------


#*Pantallas
#---------------------------------------------------------------------------------------------
#Busca todas las pantallas disponibles
def SearchScreens():
    WriteLog("Buscando pantallas")
    Clear()
    screensDir = ReadConfig(config, "screens", "screens")
    try:
        screens = listdir(screensDir)
        bar = Bar(f"{round(time()-inicialTime, 4)}: Recopilando Pantallas: ", fill="X", max=len(screens))
        for screen in screens:
            WriteLog(f"Recopilando pantallas: {screen}")
            bar.next()
            sleep(0.1)
        bar.finish()
        WriteLog("Busqueda de pantallas realizado correctamente")
        print(f"{round(time()-inicialTime, 4)}: Busqueda de pantallas realizado correctamente") #!
        return screens
    except FileNotFoundError:
        WriteLog("ERROR     No se encontro la carpeta de pantallas")
        return None

#Muestra las pantallas disponibles por pantalla
def ShowScreens(screens):
    WriteLog("Mostrando pantallas")
    screenNum = 1
    
    if (len(screens) == 1):
        print(Fore.GREEN+f"Hay {len(screens)} pantalla") #!
    else:
        print(Fore.GREEN+f"Hay {len(screens)} pantallas") #!
    print(Fore.WHITE+"0:" + Fore.MAGENTA+" Atras")
    for screen in screens:
        WriteLog(f"Mostrando pantalla: {screen}")
        print(Fore.WHITE+f"{screenNum}:" + Fore.MAGENTA+f" {screen}") #!
        screenNum = screenNum + 1

#Reconectar a una pantalla
def ReconectScreen():
    WriteLog("Reconectando a una pantalla")
    screens = SearchScreens()
    
    if (screens == None or len(screens) == 0):
        WriteLog("No hay pantallas disponibles")
        Clear()
        print(Fore.RED+f"{round(time()-inicialTime, 4)}: No hay pantallas disponibles") #!
        return None

    ShowScreens(screens)

    while True == True:
        try:
            screenToConnect = input("Introduce el numero de la pantalla a la que desea conectarse: ") #!
            screenToConnect = int(screenToConnect)
            if (screenToConnect == 0):
                WriteLog("Saliendo del menu de reconectar")
                Clear()
                break
            if (screenToConnect < 0):
                WriteLog("Pantalla introducida es negativo")
                raise IndexError
            WriteLog(f"Intentando conectar a la pantalla {screenToConnect}")
            system(f"sudo screen -r {str(screens[int(screenToConnect)-1])}") #Ejecuta el comando para conectarse a una pantalla
            Clear()
            WriteLog("Reconectando a la pantalla")
            print(Fore.BLUE+f"{round(time()-inicialTime, 4)}: Conectado Correctamente")
            WriteLog("Saliendo del menu de reconectar")
            break
        except IndexError:
            WriteLog(f"ERROR    Pantalla {screenToConnect} no existe")
            print(Fore.RED+f"{round(time()-inicialTime, 4)}: Pantalla {screenToConnect} no existe") #!
        except ValueError:
            WriteLog(f"ERROR    Valor {screenToConnect} no es un numero")
            print(Fore.RED+f"{round(time()-inicialTime, 4)}: Valor introducido no es un numero, {screenToConnect}, revise y vuelva a intentar") #!

#Eliminar una pantalla
def DeleteScreen():
    WriteLog("Eliminando una pantalla")
    screens = SearchScreens()
    
    if (screens == None or len(screens) == 0):
        WriteLog("No hay pantallas disponibles")
        Clear()
        print(Fore.RED+f"{round(time()-inicialTime, 4)}: No hay pantallas disponibles") #!
        return None

    ShowScreens(screens)

    while True == True:
        try:
            screenToConnect = input("Introduce el numero de la pantalla que desea eliminar: ") #!
            screenToConnect = int(screenToConnect)
            if (screenToConnect == 0):
                WriteLog("Saliendo del menu de eliminar")
                Clear()
                break
            if (screenToConnect < 0):
                WriteLog("Pantalla introducida es negativo")
                raise IndexError
            spinner = Spinner(f"{round(time()-inicialTime, 4)}: Eliminando ")
            WriteLog("Eliminando pantalla")
            system(f"sudo kill {str(screens[int(screenToConnect)-1]).split(".")[0]}") #Ejecuta el comando para eliminar la pantalla
            for i in range(5): #Efectos no importantes
                sleep(0.1)
                spinner.next()
            spinner.finish()
            Clear()
            WriteLog("Eliminado correctamente")
            print(Fore.BLUE+f"{round(time()-inicialTime, 4)}: Eliminado Correctamente")
            WriteLog("Saliendo del menu de eliminar")
            break
        except IndexError:
            WriteLog(f"ERROR    Pantalla {screenToConnect} no existe")
            print(Fore.RED+f"{round(time()-inicialTime, 4)}: Pantalla {screenToConnect} no existe") #!
        except ValueError:
            WriteLog(f"ERROR    Valor {screenToConnect} no es un numero")
            print(Fore.RED+f"{round(time()-inicialTime, 4)}: Valor introducido no es un numero, {screenToConnect}, revise y vuelva a intentar") #!
#---------------------------------------------------------------------------------------------


#*Archivo de Configuracion
#---------------------------------------------------------------------------------------------
#Escribe el archivo de configuracion
def WriteConfig():
    WriteLog("Escribiendo archivo de configuracion")
    apiKey = input("Introduce el token de PushBullet: ")
    WriteLog(f"Token de pushbullet: {apiKey}")
    #Datos por defecto no cambiar nada si no conoces los datos
    defaultConfig = ["[pushbullet]\n", f"apikey={apiKey} \n;Si cambiaste de toquen cambia esto por el token nuevo\n"
                     , "stoptext=No hemos podido detectar el servidor, posiblemente no este encendido, intentaremos a encenderlo.\n"
                     , "hardstoptext=Hemos detectado muchas caidas del servidor en un periodo de tiempo, no abriremos el servidor.\n","\n"
                     , "[general]\n", "maintenance=False \n;Pon True si estas haciendo mantenimiento o para el script\n", "processname=vServer\n"
                     , "stoplimit=3 \n;Cuantas veces se puede detener el servidor antes de parar el script\n", f"bin={abspath("./")}/Bin\n", "\n"
                     , "[config]\n", f"config={abspath("./")}/Config/config.ini \n;Si cambiaste la ruta del fichero de configuracion cambia esta ruta\n", "\n"
                     , "[time]\n", "secondscheck=10 \n;cada cuanto comprueba el estado del servidor\n"
                     , "secondsreset=1800 \n;cada cuanto se reinicia el contador para parar el script\n", "\n"
                     , "[screens]\n", "screenapt=/usr/bin/screen\n", "screens=/run/screen/S-root\n"]
    WriteLog(f"Configuracion inicial del archivo de configuracion: {defaultConfig}")
    #Crea el archivo
    WriteLog("Creando archivo de configuracion")
    with open("./Config/config.ini", "w+") as file:
        file.writelines(defaultConfig)
        file.close()
        print(f"{round(time()-inicialTime, 4)}: Fichero de configuracion creado correctamente") #!
    WriteLog("Modificando permisos de la carpeta")
    chmod("./Config", 0o777)
    chmod("./Config/config.ini", 0o777)

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
        print(Fore.RED+f"{round(time()-inicialTime, 4)}: Seccion {section} no se encuentra en el fichero {file}") #!
    except FileNotFoundError:
        WriteLog("ERROR     El fichero de configuracion no existe, probar eliminar el directorio de configuracion")
        print(Fore.RED+f"{round(time()-inicialTime, 4)}: El fichero {file} no existe") #!

#Funcion absoluta para conseguir la ruta del archivo de configuracion, devuelve la ruta del archivo de configuracion
def ConfigConfig():
    file = "./Config/config.ini"
    section = "config"
    datos = ReadConfig(file, section, "config")
    return datos
#---------------------------------------------------------------------------------------------


#*Menu
#---------------------------------------------------------------------------------------------
#Desplegar el menu
def Menu():
    WriteLog("Desplegar menu")
    #Menu principal, ampliable si se confiugran mas opciones
    print(Fore.CYAN+"""
    1 - Empezar el Programa
    2 - Volver a una Pantalla
    3 - Eliminar una Pantalla
    4 - Salir
    """) #!

    try:
        option = input("Escriba su opción: ") #!
        option = int(option)
    except ValueError:
        WriteLog(f"ERROR    Valor introducido {option} no es un numero")
        Clear()
        print(f"{round(time()-inicialTime, 4)}: Error de Valor, '{option}', no es un numero")
        return None

    match option:
        case 1:
            StartProgram()
        case 2:
            ReconectScreen()
        case 3:
            DeleteScreen()
        case 4:
            WriteLog("Saliendo")
            Clear()
            exit()
        case _:
            WriteLog(f"ERROR    Opcion {option} no coincide con ninguna opcion")
            Clear()
            print(f"{round(time()-inicialTime, 4)}: Opcion introducida no coincide con ninguna opcion")
#---------------------------------------------------------------------------------------------

if (not exists("./logs")):
    mkdir("./logs/")
    WriteLog("Creando directorio de logs")
    print(f"Directorio de logs generado") #!

#*Main
#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    WriteLog("\n")
    WriteLog("AutoRun ejecutado")
    inicialTime = time()

    init(autoreset=True) #Iniciar el Colorama y restablece los colores de la consola cada vez

    #Comprobar que se este ejecutando como superusuario
    if (geteuid() == 0):
        CheckConfig()

        parser = ConfigParser()
        config = ConfigConfig()

        Clear()
        CheckDependencies()
        
        Clear()
        sleep(0.5)
        while True == True:
            WriteLog("Menu abierto")
            Menu()
    else:
        WriteLog("ERROR     no se ejecuto con superusuario")
        print(Fore.RED+f"{round(time()-inicialTime, 4)}: Ejecuta con Superusuario") #!
#---------------------------------------------------------------------------------------------