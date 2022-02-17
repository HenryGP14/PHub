# http://micaminomaster.com.co/grafo-algoritmo/todo-trabajar-grafos-python/

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

from distutils.command.build import build
import math
from tkinter import filedialog
import random


class Nodo:

    def __init__(self, id, x, y, capacidad):
        self.id = id
        self.coordenada_x = x
        self.coordenada_y = y
        self.capacidad = capacidad


class Grafo:

    def __init__(self, cantidad_combinaciones):
        # Crear un diccionario de todas las combinaciones
        self.conjunto_datos = []
        self.Nodos = []
        self.numero_de_hub = 1
        self.cantidad_nodos = 0
        self.capacidad_del_hub = 0
        self.soluciones = []
        self.conjunto_soluciones = []
        self.cantidad_combinaciones = cantidad_combinaciones

    def cargar_datos_txt(self):
        archivo = filedialog.askopenfile()
        datos = open(archivo.name, "r")

        with datos as f_obj:
            for line in f_obj:
                temp = line.rstrip().split()
                self.conjunto_datos.append(list(map(int, temp)))

        self.conjunto_datos.remove([])

        configuracion_del_grafo = self.conjunto_datos.pop(0)
        self.cantidad_nodos = configuracion_del_grafo[0]
        self.numero_de_hub = configuracion_del_grafo[1]
        self.capacidad_del_hub = configuracion_del_grafo[2]

        self.convertir_datos_a_nodos()
        #
        print("Configuración del Grafo:")
        print("  Nº de nodos: " + str(self.cantidad_nodos))
        print("  Nº de hubs: " + str(self.numero_de_hub))
        print("  Capacidad de los hubs: " + str(self.capacidad_del_hub))
        print()

    def resolver_phub(self):
        self.generar_combinatoria()
        reparto = 0
        distancia_optima = 0
        solucion_index = 0

        for x in range(self.cantidad_combinaciones):
            hubs = self.elegir_hubs_aleatorios(self.soluciones[x])
            clientes = self.soluciones[x]

            suma_demandas = 0
            for a in clientes:
                suma_demandas = suma_demandas + self.Nodos[a - 1].capacidad

            reparto = math.ceil(suma_demandas / self.numero_de_hub)
            distancia_total = self.enlazar_hub_clientes(
                hubs, clientes, reparto)  # soluciones[ [], [] ]

            if (x == 0):
                distancia_optima = distancia_total
            else:
                if (distancia_optima > distancia_total):
                    distancia_optima = distancia_total
                    solucion_index = x

            self.conjunto_soluciones.append([
                hubs, clientes, distancia_total
            ])  # -> [ [hubs_1, clientes_1, distancia_total], ... ]

        print("La solución más optima es:")
        print("Hubs: ")
        print(self.conjunto_soluciones[solucion_index][0])
        print("Clientes: ")
        print(self.conjunto_soluciones[solucion_index][1])
        print("Distancia: ")
        print(self.conjunto_soluciones[solucion_index][2])

        self.dibujar_conexiones(self.conjunto_soluciones[solucion_index][0],
                                self.conjunto_soluciones[solucion_index][1],
                                reparto)

    def enlazar_hub_clientes(self, hubs, clientes, reparto):
        hub_index = 0
        demanda = 0
        suma_distancias = 0

        for x in clientes:
            if ((demanda + self.Nodos[x - 1].capacidad) <= reparto):
                demanda = demanda + self.Nodos[x - 1].capacidad
            else:
                demanda = 0
                hub_index += 1

            hub = hubs[hub_index]
            distancia = self.calcular_distancia_entre_nodos(
                self.Nodos[x - 1], self.Nodos[hub - 1])
            suma_distancias = suma_distancias + distancia
        return suma_distancias

    def dibujar_conexiones(self, hubs, clientes, reparto):
        hub_index = 0
        demanda = 0
        print()
        print("Hubs       Clientes        Distancia")
        for x in clientes:
            if ((demanda + self.Nodos[x - 1].capacidad) <= reparto):
                demanda = demanda + self.Nodos[x - 1].capacidad
            else:
                demanda = 0
                hub_index += 1

            nodo_hub = self.Nodos[hubs[hub_index] - 1]
            nodo_cliente = self.Nodos[x - 1]
            distancia = self.calcular_distancia_entre_nodos(
                nodo_cliente, nodo_hub)
            print(
                str(nodo_hub.id) + "(" + str(nodo_hub.coordenada_x) + "," +
                str(nodo_hub.coordenada_y) + ")   " + str(nodo_cliente.id) +
                "(" + str(nodo_cliente.coordenada_x) + "," +
                str(nodo_cliente.coordenada_y) + ")      " + str(distancia))

    def generar_combinatoria(self):
        x = 0
        # Este ciclo genera n combinaciones: [ [solucion_1], [solucion_2], ..., [solucion_n] ]
        while (x < self.cantidad_combinaciones):
            nodos = []
            j = 0
            # Este ciclo genera una solucion de [1 a n_datos del conjunto nodos]
            while (j < self.cantidad_nodos):
                nodo = random.randint(1, self.cantidad_nodos)
                if (self.validar_combinacion_unica(nodo, nodos)):
                    nodos.append(nodo)
                    j += 1
            if (self.validar_combinacion_unica(nodos, self.soluciones)):
                self.soluciones.append(nodos)
                x += 1

    def elegir_hubs_aleatorios(self, lista):
        hubs = []
        x = 0
        while (x < self.numero_de_hub):
            rand = random.randint(0, len(lista) - 1)
            hub = lista.pop(rand)
            hubs.append(hub)
            x += 1
        return hubs

    def validar_combinacion_unica(self, x, lista):
        for nodo in lista:
            if (x == nodo):
                return False
        return True

    def convertir_datos_a_nodos(self):
        for x in self.conjunto_datos:
            nodo = Nodo(x[0], x[1], x[2], x[3])
            self.Nodos.append(nodo)

    def calcular_distancia_entre_nodos(self, cliente, hub):
        # Resta de vectores
        vector_coor_x = cliente.coordenada_x - hub.coordenada_x
        vector_coor_y = cliente.coordenada_y - hub.coordenada_y

        # Calcular la magnitud del vector (hipotenusa)
        return math.hypot(vector_coor_x, vector_coor_y)


md = Grafo(10)  # Grafo(num_interacciones)
md.cargar_datos_txt()
md.resolver_phub()