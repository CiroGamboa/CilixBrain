import math
def MPM(subgrafo):
    nodos = len(subgrafo)
    matching = []
    R = []

    for i in range(nodos):
        menor = 999
        for j in range (nodos - 1):
            if i != j and i not in R and j not in R:
                if subgrafo[i][j] < menor:
                    menor = subgrafo[i][j]
                    a, b = i, j
                    R.append(a)
                    R.append(b)
                    if [a,b] not in matching:
                        matching.append((a, b))

    return matching
