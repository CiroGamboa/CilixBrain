def rutaEuleriana(subgrafo):
    #siempre inicia en 0
    ruta = []
    for n in subgrafo:
        if len(subgrafo[n]) > 0:
            ini = n
            while len(ruta) < 2*len(subgrafo):
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
    if not not final: #para evitar errores cuando entra una lista vacia
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
    else:
        return []
