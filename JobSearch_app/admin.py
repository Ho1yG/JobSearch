from django.contrib import admin
from .models import Company, Vacancy, Applicant

# Регистрация моделей в административном интерфейсе
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Applicant)
