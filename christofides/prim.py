def MST(matrizAdyacencia):
    R = [] #vertices ya evaluados
    P = [] #aristas del arbol recubridor minimo
    R.append(0); #vertice inicial
    nodos = len(matrizAdyacencia)

    while len(R) < nodos: #hasta que ya se han revisado todos los vertices
        d = []
        for v in R:
            for i in range(nodos):
                if i not in R and matrizAdyacencia[v][i] != 0:
                    #se agregan las posibilidades segun
                    #los vertices que lleva el arbol
                    d.append([v, i])
        #se busca la distancia mas corta entre las posibilidades
        menor = 9999
        for c in d:        
            if matrizAdyacencia[c[0]][c[1]] <= menor:
               menor = matrizAdyacencia[c[0]][c[1]]
               arista = (c[0], c[1])
        P.append(arista)
        R.append(arista[1])

    return P
