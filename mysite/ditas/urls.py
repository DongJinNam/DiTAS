from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^%', views.index, name='index'),
	url(r'^keyboard/',views.keyboard),
	url(r'^message',views.message),	
]
