from django.urls import path
from .import views 

urlpatterns = [
    
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
]