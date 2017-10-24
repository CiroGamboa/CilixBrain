import math
from christofides.prim import MST
from christofides.minimumPerfectMatching import MPM
from christofides.rutaEulerianaConShortcut import rutaEuleriana
from christofides.calculoDistancia import distanciaTotal

#recibe una matriz de adyacencia
def Christofides(MA):
    
    nodos = len(MA)
    arbol = MST(MA) #arbol recubridor minimo
    
    grados = [0]*(len(arbol) + 1)
    for c in arbol:
        grados[c[0]] += 1
        grados[c[1]] += 1

    subgrafo = []
    verticesImpares = [] #vertices del subgrafo de impares

    #matriz de adyacencia del nuevo grafo con los vertices impares
    for f in range(nodos):
        if grados[f]%2 != 0:
            verticesImpares.append(f) 
            temp = []
            for c in range(nodos):
                if grados[c]%2 != 0:
                    #evita repetir aristas en mst
                    if (f,c) in arbol or (c,f) in arbol:
                        temp.append(math.inf)
                    else:
                        temp.append(MA[f][c])
            if len(temp) != 0:
                subgrafo.append(temp)

    euleriano = arbol
    if len(verticesImpares) > 0:
        mpm = MPM(subgrafo) #minimum perfect-matching
        for v in mpm:
            #cambia las etiquetas a las originales
            i, j = v
            v = (verticesImpares[i], verticesImpares[j])
            #if v not in euleriano and v[::-1] not in euleriano:
            euleriano.append(v) #agrega el mpm al mst e
    
    #Encuentra la ruta que pasa por todas las aristas recorriendo el grafo euleriano
    LA = {}
    for i in range(nodos):
        LA[i] = []

    for a in euleriano:
        x, y = a
        LA[x].append(y)
        LA[y].append(x)

    #por si acaso
    for e in LA:
        #se ordena segun el peso en la matriz de adyacencia
        LA[e] = sorted(LA[e], key=lambda x: MA[e][x])

    ruta = rutaEuleriana(LA)
    return ruta, distanciaTotal(ruta, MA)
