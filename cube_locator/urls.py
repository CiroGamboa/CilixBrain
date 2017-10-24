from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^main/$', views.get_main),
	#url(r'^getRuta/(?P<angsDist>[0-9]+)/$', views.get_vector),
	url(r'^index/$', views.get_index),
	url(r'^video/(?P<n>[0-9]+)/$', views.get_video),
	url(r'^ruta/(?P<video>[0-9]+)/$', views.get_ruta),
	url(r'^about/$', views.get_about),
]