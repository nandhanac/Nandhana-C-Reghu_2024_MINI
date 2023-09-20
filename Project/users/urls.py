from django.urls import path
from .views import home, profile, RegisterView,index,about,admin_dashboard_view,mechanic_dashboard_view

urlpatterns = [
     path('', index, name='index'),
    path('home/', home, name='users-home'),

    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('about/',about,name='about'),
    path('admin-dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('mechanic-dashboard/',mechanic_dashboard_view, name='mechanic-dashboard'),
    
]
