from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home_url'),
    path('register/', views.registerView, name='register_url'),
    path('login/', views.logInView, name='login_url'),
    path('logout/', views.logOutView, name='logout_url'),
]
