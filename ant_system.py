'''
Aspecto General 

Implementación del algoritmo de ant_system para resolver el camino mas corto
-> Usa una matriz de visibilidad ( )
-> Usa una matriz de distancias
-> Usa una matriz de feromonas
-> Se determina el número de hormigas
-> Se determina el número de iteraciones
-> Usa 4 variables constantes  ( alfa, beta, rho, Q ) 
-> Se inicializa con algun valor la matriz de feromonas

------------------------------------------------------------------

Aspectos que se pueden mejorar 

-> Usar un diccionario para las 3 matrices para mejorar rendimiento
-> Se puede aplicar una matriz tringular para las tres matrices
-> generar un diccionario mas que posea la multiplicacion de matriz feromonas * matriz_visibilidad
-> Se puede evitar la generación de valor aleatorio como su calculo en el ultimo camino, pero con el fin de 
   seguir el algoritmo se mantiene este calculo

Caso diccionarios : buscar primero el indice menor y luego el mayor para la busqueda de algun valor 
en el diccionario.

    matriz que solo requiere la triangulización superior
    A     B     C     D     E .....
A  nan    x     x     x     x 
B  nan   nan    x     x     x   
C  nan   nan   nan    x     x
D  nan   nan   nan    nan   x
E  nan   nan   nan    nan   x
.
.
.
'''
import numpy as np
import math
import random

diccionario = [[0., 12.,  3., 23.,  1.,  5., 23., 56., 12., 11., ],
               [12.,  0.,  9., 18.,  3., 41., 45.,  5., 41., 27., ],
               [3.,  9.,  0., 89., 56., 21., 12., 48., 14., 29., ],
               [23., 18., 89.,  0., 87., 46., 75., 17., 50., 42., ],
               [1.,  3., 56., 87.,  0., 55., 22., 86., 14., 33., ],
               [5., 41., 21., 46., 55.,  0., 21., 76., 54., 81., ],
               [23., 45., 12., 75., 22., 21.,  0., 11., 57., 48., ],
               [56.,  5., 48., 17., 86., 76., 11.,  0., 63., 24., ],
               [12., 41., 14., 50., 14., 54., 57., 63.,  0.,  9., ],
               [11., 27., 29., 42., 33., 81., 48., 24.,  9.,  0.]]

letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


class Ant_system(object):
    def __init__(self, cantidad_hormigas, matriz_distancias):
        self.matriz_distancias = np.array(matriz_distancias)
        self.cantidad_hormigas = cantidad_hormigas
        self.hormigas = np.zeros([cantidad_hormigas, 10]).astype(int)

    def generar_matriz_visibilidad(self):
        self.matriz_visibilidad = np.zeros([10, 10])
        for i in range(10):
            for j in range(10):
                if(i != j):
                    self.matriz_visibilidad[i][j] = np.round(
                        1/self.matriz_distancias[i][j], 6)

    def inicializar_matriz_feromonas(self, valor):
        self.matriz_feromonas = np.zeros([10, 10])
        for i in range(10):
            for j in range(10):
                if(i != j):
                    self.matriz_feromonas[i][j] = valor

    def set_iteraciones(self, iteraciones):
        self.iteraciones = iteraciones

    def set_alfa(self, alfa):
        self.alfa = alfa

    def set_beta(self, beta):
        self.beta = beta

    def set_rho(self, rho):
        self.rho = rho

    def set_quo(self, quo):
        self.quo = quo

    def generar_ciudad_inicial(self):
        np.random.seed(0)
        self.ciudad_inicial = np.random.randint(0, 10)

    def imprimir(self, matriz):
        row = " {:<7} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} | {:<10s} |".format
        print(row('estados', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'))
        for fila in range(10):
            row = " {:<7} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} | {:^10f} |".format
            print(row(letras[fila], matriz[fila][0], matriz[fila][1], matriz[fila][2], matriz[fila][3], matriz[fila]
                      [4], matriz[fila][5], matriz[fila][6], matriz[fila][7], matriz[fila][8], matriz[fila][9]))

    def imprimir_parametros(self):
        print('Parámetros:')
        print(f'Cantidad de Hormigas : {self.cantidad_hormigas}')
        print(f'Feromona Inicial : 0.1')
        print(f'Alfa : {self.alfa}')
        print(f'Beta : {self.beta}')
        print(f'Rho : {self.rho}')
        print(f'Q : {self.quo}')
        print(f'Cantidad de iteraciones : {self.iteraciones}')

    def inicializar(self):
        self.imprimir_parametros()
        self.inicializar_matriz_feromonas(0.1)
        self.generar_matriz_visibilidad()
        self.generar_ciudad_inicial()
        print('\n Matriz de Distancias\n')
        self.imprimir(self.matriz_distancias)
        print('\n Matriz de Visibilidad\n')
        self.imprimir(self.matriz_visibilidad)

    def caminar(self, posicion,  caminos):
        suma = 0
        for camino in caminos:
            t = self.matriz_feromonas[posicion][camino]**self.alfa
            n = self.matriz_visibilidad[posicion][camino]**self.beta
            self.matriz_multiplicada[posicion][camino] = t * n
            calc = self.matriz_multiplicada[posicion][camino]
            print(
                f'{letras[posicion]}-{letras[camino]} ; t = {t} ; n = {n} ; t*n = {calc}')
            suma += calc
        print(f'Suma: {suma}')
        posicion_a_escoger = 0
        aleatorio = np.random.uniform()
        camino_escogido = -1
        flag = True
        for camino in caminos:
            prob = self.matriz_multiplicada[posicion][camino]/suma
            print(f'{letras[posicion]}-{letras[camino]} ; prob = {prob}')
            posicion_a_escoger += prob
            if(aleatorio <= posicion_a_escoger and flag == True):
                camino_escogido = camino
                flag = False

        print(f'Numero aleatoria para la probaabilidad = {aleatorio}')
        print(f'Camino Escogido: {letras[camino_escogido]}')
        return camino_escogido

    def imprimir_camino(self, recorrido):
        linea = ''
        for ciudad in range(recorrido.size):
            if(ciudad != recorrido.size-1):
                linea += letras[recorrido[ciudad]] + ' - '
            else:
                linea += letras[recorrido[ciudad]]
        return linea

    def camino_hormiga(self, n_hormiga):
        print(f'\nHormiga {n_hormiga+1}')
        print(f'Ciudad_Inicial : {letras[self.ciudad_inicial]}')
        caminos = list(range(10))
        caminos.remove(self.ciudad_inicial)
        # random.shuffle(caminos)
        posicion = self.ciudad_inicial
        iterador = 0
        self.hormigas[n_hormiga][iterador] = posicion
        while len(caminos) > 0:
            iterador += 1
            camino_escogido = self.caminar(posicion, caminos)
            caminos.remove(camino_escogido)
            posicion = camino_escogido
            self.hormigas[n_hormiga][iterador] = posicion
            print()
        print(
            f'Hormiga {n_hormiga+1 } ---> {self.imprimir_camino(self.hormigas[n_hormiga])}')
        print('--------------------------------------------------------------------------------')

    def calcular_costo(self, hormiga):
        suma = 0
        for camino in range(hormiga.size-1):
            suma += self.matriz_distancias[hormiga[camino],hormiga[camino+1]]
        return suma

    def mostrar_hormigas(self):
        costos = []
        for hormiga in range(self.cantidad_hormigas):
            costo = self.calcular_costo(self.hormigas[hormiga])
            costos.append(costo)
            print(
                f'Hormiga {hormiga+1} ({self.imprimir_camino(self.hormigas[hormiga])}) - Costo : {costo }')
        return costos

#busca un camino para un recorrido en específico
#retorna 0 - no encontrado y 1 - encontrado:
    def buscar(self, camino1, camino2, recorrido):
        for ciudad in range(9):
            if(recorrido[ciudad] == camino1 or recorrido[ciudad] == camino2):
                if(recorrido[ciudad+1] == camino2 or recorrido[ciudad+1] == camino1):
                    return 1
                else:
                    return 0
        return 0

# proceso de cambio de feromonas
    def actualizar_feromonas(self, costos):
        nuevas_feromonas = np.zeros([10, 10])
        for fila in range(10):
            for columna in range(10):
                if(fila != columna):
                    suma = 0
                    out = ''
                    for hormiga in range(self.cantidad_hormigas):
                        a = self.buscar(fila, columna, self.hormigas[hormiga])
                        if a:
                            valor = self.quo/costos[hormiga]
                            suma += valor
                        else:
                            valor = 0

                        if(hormiga != self.cantidad_hormigas-1):
                            out += str(valor) + '+'
                        else:
                            out += str(valor)
                    n_p = self.matriz_feromonas[fila][columna] * self.rho
                    suma += n_p
                    print(
                        f'{letras[fila]}-{letras[columna]}: Feromona = {n_p} + {out} = {suma} ')
                    nuevas_feromonas[fila][columna] = suma

        self.matriz_feromonas = nuevas_feromonas

# Proceso de iteracion
    def iteracion(self, n_iteracion):
        print(f'\nIteracion: {n_iteracion}')
        print()
        print('\n Matriz de Visibilidad\n')
        self.imprimir(self.matriz_visibilidad)
        print('\n Matriz de Feromonas\n')
        self.imprimir(self.matriz_feromonas)
        self.matriz_multiplicada = self.matriz_visibilidad * self.matriz_feromonas
        for n_hormiga in range(self.cantidad_hormigas):
            self.camino_hormiga(n_hormiga)

# Proceso en general
    def run(self):
        self.inicializar()
        for iteracion in range(1, self.iteraciones+1):
            self.iteracion(iteracion)
            costos = self.mostrar_hormigas()
            self.actualizar_feromonas(costos)
        print('\n Matriz de Distancia\n')
        self.imprimir(self.matriz_distancias)
        print('\n Matriz de Visibilidad\n')
        self.imprimir(self.matriz_visibilidad)
        print('\n Matriz de Feromonas\n')
        self.imprimir(self.matriz_feromonas)
        print('\n Hormigas\n')
        self.mostrar_hormigas()


if __name__ == "__main__":
    sistema = Ant_system(5, diccionario)
    sistema.set_alfa(1)
    sistema.set_beta(1)
    sistema.set_rho(0.99)
    sistema.set_quo(1)
    sistema.set_iteraciones(200)
    sistema.run()
