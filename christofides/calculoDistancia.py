def distanciaTotal(ruta, MA):
    d = len(ruta)
    total = 0
    for i in range(d-1):
        total += MA[ruta[i]][ruta[i+1]]
    return total
