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

    if len(verticesImpares) > 0:
        mpm = MPM(subgrafo) #minimum perfect-matching
        euleriano = arbol
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

##g = [[0, 3.61, 7.21, 3, 4.47, 4.24, 4.47],[3.61, 0, 6.380977613272764, 3.997003984913176, 5.546819396892034, 5.80238127553172, 6.390322949509599], [7.21, 6.380977613272764, 0, 6.577677499089561, 7.5060120031856385, 8.008033009905796, 8.743590116131454], [3, 3.997003984913176, 6.577677499089561, 0, 4.114373808871548, 4.222274001020345, 4.7846512306011055], [4.47, 5.546819396892034, 7.5060120031856385, 4.114373808871548, 0, 4.464674238727974, 4.899422796339998], [4.24, 5.80238127553172, 8.008033009905796, 4.222274001020345, 4.464674238727974, 0, 4.47641324504131], [4.47, 6.390322949509599, 8.743590116131454, 4.7846512306011055, 4.899422796339998, 4.47641324504131, 0]]
##
##
##ruta, distancia = Christofides(g)
##print(ruta)
##print(distancia)
