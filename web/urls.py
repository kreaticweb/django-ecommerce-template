from django.urls import path, re_path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    
]
