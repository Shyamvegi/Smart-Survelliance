from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name = 'index'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('login/',views.logoutUser,name='logout'),
    path('performAction/',views.performAction,name="performAction"),
]
