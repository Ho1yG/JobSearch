from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test


def user_is_company(user):

    return user.is_company

urlpatterns = [
    path('', views.homeView, name='home_url'),
    path('vacancies/', views.vacanciesView, name='vacancies'),
    path('applicants/', views.aplicantsView, name='applicants_url'),
    path('applicant/<int:applicant_id>/', views.applicant_detail_view, name='applicant_detail_url'),
    path('delete_applicant/<int:applicant_id>/', views.delete_applicant_view, name='delete_applicants_url'),
    path('vacancy_detail/<int:vacancy_id>/', views.vacancyDetail, name='vacancy_detail_url'),
    path('create_vacancy/', user_passes_test(user_is_company)(views.createVacancyView),
         name='create_vacancy_url'),
    path('register/', views.registerView, name='register_url'),
    path('register_company/', views.registerCompanyView, name='register_company_url'),
    path('delete_user/', views.delete_user_view, name='delete_user_url'),
    path('login/', views.logInView, name='login_url'),
    path('logout/', views.logOutView, name='logout_url'),
    path('profile/', views.profileView, name='profile_url'),
    path('company_profile/', user_passes_test(user_is_company)(views.companyProfileView),
         name='company_profile_url'),
    path('update_vacancy/<int:vacancy_id>/', user_passes_test(user_is_company)(views.updateVacancyView),
         name='update_vacancy_url'),
    path('delete_vacancy/<int:vacancy_id>/', user_passes_test(user_is_company)(views.deleteVacancyView),
         name='delete_vacancy_url'),
    path('view_vacancy_url/<int:vacancy_id>/', views.viewVacancyView, name='view_vacancy_url'),
    path('view_vacancy_user_url/<int:applicant_id>/', views.viewUserVacancyView,
         name='view_vacancy_user_url'),
    path('delete_account/', views.delete_account_view, name='delete_account_url'),
    path('change_application_status/<int:applicant_id>/',
         user_passes_test(user_is_company)(views.change_application_status_view),
         name='change_application_status_url'),


]
