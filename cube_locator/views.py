from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from cube_locator.medidorDistancia8 import medidorDistancia
from christofides.COMPLETOV1 import rutaRecoleccion
#from medidorDistancia6 import medidorDistancia
import cv2

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
        context = {'n': n}
        html = TemplateResponse(request, 'video.html',context)
        return HttpResponse(html.render())

def get_ruta(request, video): #ejemplo
        array = []
        #Para el video de 5
        if video == "5":
                array = [[39.185227272727275, 16.199996948242188], [61.075367647058826, 9.878046919659864], [91.6625, 25.851058959960938], [106.96614583333333, 13.965514610553598], [142.92934782608697, 25.851058959960938]]
        #Para el de 3
        elif video == "3":
                array = [[49.40133714969243, 9.204543720592145], [95.22156954887225, 18.13432494206216], [124.06119702665765, 11.462261991680801]]

        #AGREGAR

        ruta, distancia = rutaRecoleccion(array)

        context = {'vector': str(array), 'ruta': str(ruta), 'distancia': distancia, 'video': video} 
        html = TemplateResponse(request, 'ruta.html',context)
        return HttpResponse(html.render())

def get_about(request):
        context = {}
        html = TemplateResponse(request, 'about.html',context)
        return HttpResponse(html.render())



