from django.urls import path
from .views import Home
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('home/', Home.as_view(), name="home"),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    
]
