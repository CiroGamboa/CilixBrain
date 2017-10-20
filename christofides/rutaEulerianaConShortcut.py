def rutaEuleriana(subgrafo):
    #siempre inicia en 0
    ruta = []
    for n in subgrafo:
        if len(subgrafo[n]) > 0:
            ini = n
            while True:
                ruta.append(ini)
                tmp = subgrafo[ini]
                if len(tmp) > 0:
                    ant = ini
                    ini = subgrafo[ini][0]
                    tmp.remove(ini)
                    subgrafo[ini].remove(ant)
                if ini == n:
                    break;
                
    #shortcut
    final = []
    for e in ruta:   
        if e not in final:
            final.append(e)
        else:
            final.remove(e)
            final.append(e)

    #validacion y ajustes de ruta
    if final[0] == 0:
        return final
    elif final[-1] == 0:
        final.reverse()
        return final
    else:
        l = len(final)
        i = final.index(0)
        if  l - i < i:
            tmp = final
            tmp.remove(0)
            tmp.insert(0,0)
        else:
            tmp = final[i+1::]
            tmp.reverse()
            tmp.insert(0,0)
            for e in range(i):
                tmp.append(final[i-e-1])
        return tmp
    
##a = {0: [3, 1, 6, 2], 1: [0, 2], 2: [1, 0], 3: [0, 4, 5, 6], 4: [3, 5], 5: [3, 4], 6: [0, 3]}
##a1 = {0: [1, 4], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [0, 3]}
##a2 = {0: [6, 4], 1: [3, 2], 2: [5, 1], 3: [4, 1], 4: [3, 0, 7, 5], 5: [6, 8, 2, 4], 6: [0, 5], 7: [4, 8], 8: [5, 7]}
####
##r = rutaEuleriana(a2)
##print(r)
