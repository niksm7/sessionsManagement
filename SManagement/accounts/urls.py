from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('addUser/',views.addUser),
    path('logout/',views.handleLogout),
    path('login/',views.handleLogin)
]