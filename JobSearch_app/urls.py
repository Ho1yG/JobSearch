from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home_url'),
    path('vacancies/', views.vacanciesView, name='vacancies'),
    path('vacancy_detail/<int:vacancy_id>/', views.vacancyDetail, name='vacancy_detail_url'),
    path('create_vacancy/', views.createVacancyView, name='create_vacancy_url'),
    path('register/', views.registerView, name='register_url'),
    path('register_company/', views.registerCompanyView, name='register_company_url'),
    path('login/', views.logInView, name='login_url'),
    path('logout/', views.logOutView, name='logout_url'),
    path('profile/', views.profileView, name='profile_url'),

]
