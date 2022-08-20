from django.urls import path

from . import  views


app_name = 'orientationSystem'
urlpatterns = [
    path('',views.index, name='index'),
     path('login', views.login,name='login'),
    path('profile', views.profile,name='profile'),
    path('form/', views.get_name, name='get_name'),
    path('form/predict/',views.predict,name="predict")
   
]