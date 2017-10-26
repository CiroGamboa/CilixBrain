import math
import itertools

def distanciaTotal(ruta, MA):
    d = len(ruta)
    total = 0
    for i in range(d-1):
        total += MA[ruta[i]][ruta[i+1]]
    return total

def mejorRuta(MA):
    n = len(MA)
    nodos = list(range(n))
    c = list(itertools.permutations(nodos))
    suma = math.inf

    for e in c:
        if e[0] == 0:
            d = distanciaTotal(e, MA)
            if d < suma:
                suma = d
                ruta = e
            
    return ruta, suma


    
