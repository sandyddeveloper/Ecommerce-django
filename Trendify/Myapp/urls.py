from django.urls import path
from .import views 

urlpatterns = [
    
    path('',views.Home,name='homepage'),   
    path('signup/',views.signup,name='signup'),
    path('update_user/',views.update_user,name='update_user'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>/', views.SetNewPasswordView.as_view(), name='set-new-password'),
    path('about/', views.about_view, name='about'),
    path('product/<int:pk>', views.product_view, name='product'),
    path('category/<str:nun>', views.category, name='category'),
]

