from django.urls import path

from .views import *

app_name = 'acounts'

urlpatterns = [
    path('login/',loginPage, name= 'login'),
    path('logout/',logoutUser, name= 'logout'),
    path('register/',register, name= 'register'),
]
