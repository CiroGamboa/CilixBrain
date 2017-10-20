from christofides.grafoCompleto import getGrafo
from christofides.TSPv3 import Christofides

#deteccion de objetos
#retorna diccionario de distancias y angulos
def rutaRecoleccion(g):
#g = [[7.931468531468531, 23.671875], [22.462609890109892, 18.253012048192772], [33.2706447963801, 15.947368421052628], [48.02076923076923, 31.5625], [71.41908080451658, 26.578947368421108], [88.63552884615379, 14.708737864077653], [103.57253752345198, 21.04166666666669], [127.77427572427551, 15.78125]]
    #Arma el grafo completo
    #retorna matriz de adyacencia
    MA = getGrafo(g)

    #Se ejecuta el algoritmo de Christofides
    #retorna la ruta y la distancia
    ruta, distancia = Christofides(MA)
    print(distancia)
    return ruta
