from constants import url
import requests
def userInterface():

    i = input("Bienvenido al servicio de sistema distribuido, que desea hacer? \n1. Obtener un valor \n2. Introducir un valor \n3. Eliminar un valor \n")
    if(i == "1"):
        key = input("Por favor ingrese la llave del objeto que busca\n")
        getValue(key)
    elif(i == "2"):
        key = input("Por favor ingrese la llave del objeto que desea crear o modificar\n")
        value = input("Por favor ingrese el objeto que desea crear o modificar\n")
        setValue(key, value)
    elif(i == "3"):
        key = input("Por favor ingrese la llave del objeto que busca eliminar\n")
        deleteValue(key)

def getValue(key):
    return print(requests.get(url, params="key="+ str(key)))

def setValue(key, value):
    return print(requests.post(url, data={key : value}))

def deleteValue(key):
    return print(requests.delete(url, params="key="+ str(key)))

def main():
    userInterface()

main()