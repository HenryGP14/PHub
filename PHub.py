# http://micaminomaster.com.co/grafo-algoritmo/todo-trabajar-grafos-python/

# Estructura del grafo
'''
    [
    1:[2, 5, 4, 3, 6],
    2:[1, 5, 4, 3, 6],
    3:[1, 5, 2, 4, 6],
    4:[1, 2, 3, 6, 5],
    5:[1, 2, 3, 4, 6],
    6:[1, 2, 3, 4, 5],
    ]
'''

# Notaciones del conjunto de datos
## Primera fila se presenta los datos que van en mi grafo
'''
    Primer valor es la cantidad de nodos en el grafo
    Segundo valor es el número de servidores que podemos elegir
    Tercero es la capacidad que tiene cada servidor
'''
## Demas filas
'''
    Primer valor es el número de nodo
    Seguno valor es la coordenada en x del nodo
    Tercer valor es la coordenada en y del nodo
    Cuarto valor es la demanda del cliente al servidor
'''     

# Los nodos se unan aleatoriamente

from tkinter import filedialog

class Nodo:

    def __init__(self, id, tipo):
        self.id = id
        self.coordenada_x = None
        self.coordenada_y = None
        self.capacidad = None
        self.distancia = None
        self.tipo = tipo
        self.conexiones = []  #lista de objetos nodos

    def agregar_nodo_vecino(self, nodo_vecino, tipo):
        if not nodo_vecino in self.conexiones:
            self.conexiones.append(nodo_vecino)


class Grafo:

    def __init__(self):
        # Crear un diccionario de los datos
        self.nodos = {}

    def agregar_vertice(self, vertice, tipo):
        if vertice not in self.nodos:
            self.nodos[vertice] = Nodo(vertice, tipo)

    def agregar_arista(self, vertice1, vertice2):
        if vertice1 in self.nodos and vertice2 in self.nodos:
            self.nodos[vertice1].agregar_nodo_vecino(vertice2, 'cliente')
            self.nodos[vertice2].agregar_nodo_vecino(vertice1, 'servidor')

    def cargar_datos_txt(self):
        archivo = filedialog.askopenfile()
        datos = open(archivo.name, "r")
        print(datos.read())

    def sumatoria_distancia():
        print('Aqui se calcula la suma de todas las conexiones a los servidores')

    def generar_hub_aleatorios():
        print('Aqui se generarán aleatoriamente los servidores')


md = Grafo()
md.cargar_datos_txt()