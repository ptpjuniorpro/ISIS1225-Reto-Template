import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
from App import logic as lg
from DataStructures.List import array_list as lt


def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return lg.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    first_5, last_5, time, count, catalog = lg.load_data(control)
    
    print(f"\nSe cargaron {count} elementos en {round(time,2)} ms\n")

    print("Primeros 5 elementos cargados:")
    for i in range(1, lt.size(first_5)):
        print()
        print(lt.get_element(first_5, i))

    print("\nÚltimos 5 elementos cargados:")
    for i in range(1, lt.size(last_5)):
        print()
        print(lt.get_element(last_5, i))

    print()
    return catalog


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, lat_o, lon_o, lat_d, lon_d, grulla):
    """
    Imprime la solución del Requerimiento 1:
    Los primeros 5 nodos migratorios y los últimos 5.
    """
    list = lg.req_1(control, lat_o, lon_o, lat_d, lon_d, grulla)
    print(list)



def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            lat_o = 27.0 #float(input("Ingrese la latitud de origen: "))
            lon_o = 61.0 # float(input("Ingrese la longitud de origen: "))
            lat_d = 21.0 #float(input("Ingrese la latitud de destino: "))
            lon_d = 78.0 #float(input("Ingrese la longitud de destino: "))
            grulla = 912028234 #input("Ingrese el ID de la grulla: ")
            
            print_req_1(data, lat_o, lon_o, lat_d, lon_d, grulla)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
