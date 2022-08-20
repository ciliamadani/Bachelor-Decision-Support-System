from django.urls import path

from . import  views


app_name = 'orientationSystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.get_name, name='get_name'),
    path('form/predict/',views.predict,name="predict"),
    path('form/predict2/', views.diplayVis, name="diplayVis")
]