from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from cube_locator.medidorDistancia8 import medidorDistancia
from christofides.COMPLETOV1 import rutaRecoleccion
from christofides.calculoDistancia import mejorRuta
#from medidorDistancia6 import medidorDistancia
import cv2

array = []
real = []

class JSONResponse(HttpResponse):

        def __init__(self, data, **kwargs):
                content = JSONRenderer().render(data)
                kwargs['content_type'] = 'application/json'
                super(JSONResponse, self).__init__(content, **kwargs)

def get_index(request):
        context = {}
        html = TemplateResponse(request, 'index.html',context)
        return HttpResponse(html.render())

def get_video(request, n): #numero de elementos
        global array, real
        #Para el video de 3
        if n == "3":
                array = [[36.498141627543035, 18.134324942062158], [100.33624093043105, 30.837831651842286], [119.65437940140836, 15.18749713897705]]
                real = [[33,22.2],[77,30.5],[94,16]]
        #Para el de 3
        elif n == "5":
                array = [[29.51785714285714, 19.596770501905876], [48.30952380952381, 9.848212242126465], [65.27771335807051, 26.63414075897961], [87.63265306122445, 13.806815580888228], [103.59226190476184, 30.837831651842286]]
                real = [[31,21.5],[46,10.8],[60,27.8],[83,16],[99,32.2]]
        elif n == "6":
                array = [[5.35066526610644, 16.651682821552411], [26.588662790697676, 18.999997174298311], [41.14233193277305, 22.9245239833616], [63.77083333333323, 24.83783165184227], [76.67867772108823, 25.928565979003906], [100.29501488095215, 24.837831651842286]]
                real = [[5,17.8],[26,20.6],[40.7,24.8],[60.7,26.7],[80.7,27.3],[100.6,26.4]]
        elif n == "8":
                array = [[5.545454545454547, 17.525770836269736], [20.1375, 18.13432494206214], [40.07675438596492, 13.499997456868483], [50.92538759689921, 27.3749942779541], [73.93311403508767, 21.112672832650208], [88.74621212121211, 30.153840285081102], [100.38541666666673, 10.878046919659877], [112.77559523809535, 19.285710652669273]]
                real = [[5,17.3],[20.7,21],[40.3,13.8],[50.7,27.3],[73,20.5],[88,28],[100.5,11.5],[112,25.5]]

        #calculo de error
        promErrorDist = 0
        promErrorAng = 0
        for i in range(len(real)):
                promErrorAng += round(abs(real[i][0]-array[i][0])*100/real[i][0])
                promErrorDist += round(abs(real[i][1]-array[i][1])*100/real[i][1])

        promErrorDist = promErrorDist/(i+1)
        promErrorAng = promErrorAng/(i+1)
        
        promErrorDist = round(promErrorDist, 2)
        promErrorAng = round(promErrorAng, 2)
 
        context = {'n': n, 'ea': promErrorAng, 'ed': promErrorDist}
        html = TemplateResponse(request, 'video.html',context)
        return HttpResponse(html.render())

def get_ruta(request, video): #ejemplo
        global array
        ruta, distancia, MA = rutaRecoleccion(array)
        mr = []

        #Calcula todas las posibles rutas y la que tiene la menor distancia
        mejorR, mejorD = mejorRuta(MA)
        print(mejorR, mejorD)
        error = round(abs(mejorD-distancia)*100/mejorD,1)

        for e in MA:
                mr.append([round(elem, 1) for elem in e ])
        distancia = round(distancia, 1)

        context = {'vector': str(array), 'ruta': str(ruta), 'distancia': distancia, 'video': video, 'MatAdy': mr, 'mejorRuta': mejorR, 'mejorDistancia': mejorD, 'error': error} 
        html = TemplateResponse(request, 'ruta.html',context)
        return HttpResponse(html.render())

def get_about(request):
        context = {}
        html = TemplateResponse(request, 'about.html',context)
        return HttpResponse(html.render())



