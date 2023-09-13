from django.urls import path
from .views import home, profile, RegisterView,index,about

urlpatterns = [
     path('', index, name='index'),
    path('home/', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('about/',about,name='about'),
]
