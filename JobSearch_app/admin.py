from django.contrib import admin
from .models import WorkType, Category, Vacancy, Applicant

# Регистрация моделей в административном интерфейсе

admin.site.register(WorkType)
admin.site.register(Category)
admin.site.register(Vacancy)
admin.site.register(Applicant)
