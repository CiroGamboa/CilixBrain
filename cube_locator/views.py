from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

def get_main(request):
	context = {}
	html = TemplateResponse(request, 'index.html',context)
	return HttpResponse(html.render())

