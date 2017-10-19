from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from cube_locator.medidorDistancia6 import medidorDistancia
import cv2


# Se carga la imagen de referencia tan pronto se lanza
# el servidor para ahorrar tiempo
imgRef = cv2.imread('images/cubo_rojo_15cm.jpg')
imgRef = cv2.resize(imgRef, (800,448), interpolation = cv2.INTER_AREA)
rectRef = medidorDistancia.get_dist_ref(imgRef)

def get_main(request):
	video = cv2.VideoCapture("videos/mul_red_cubes_1.MOV")

	pixError = 20
	rotationDir = 'right'
	thickWindowCube = 200
	thickWindowDetect = 10
	umbralIn = 20
	umbralOut = 5
	med = medidorDistancia(pixError,rotationDir,thickWindowCube,thickWindowDetect,umbralIn,umbralOut,rectRef)
	med.track_cubos(video)
	angs_dists = med.get_angs_dists()

	context = {'angs_dists':angs_dists}
	html = TemplateResponse(request, 'index.html',context)
	return HttpResponse(html.render())

