#dic es un diccionario que incluye el angulo y la distancia
#ej: {0: [30, 5], ...}
import math
def getGrafo(dic):
    nodos = len(dic)
    MA = []
    MA.append([])
    MA[0].append(0)
    
    #crea la matriz de adyacencia
    for i in range(0, nodos):
        MA[0].append(dic[i][1])
        MA.append([])
        MA[i+1].append(dic[i][1])
        
    for j in range(0, nodos):
        for i in range(0, nodos):          
            #distancia equivalente
            if i == j:
                d = 0
            else:
                #distancias
                d1 = dic[i][1]
                d2 = dic[j][1]
                #angulo
                a = abs(dic[i][0] - dic[j][0])*(math.pi/180)
                d = math.sqrt(pow(d1,2) + pow(d2,2) - d1*d2*math.cos(a))
            MA[i+1].append(d)
        
    return MA

##g = [[34,3.61], [55,7.21], [90,3], [116,4.47], [134,4.24], [153,4.47]]
##print(getGrafo(g))
