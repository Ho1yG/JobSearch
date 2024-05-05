from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    birth_date = models.CharField(max_length=10, blank=True)
    specialty = models.CharField(max_length=20, blank=True)
    experience = models.PositiveIntegerField(default=0)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=15, blank=True)
    company_address = models.CharField(max_length=25, blank=True)
    industry = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=200, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    category_name = models.CharField(max_length=100)

class WorkType(models.Model):
    type_name = models.CharField(max_length=100)



class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expyear = models.IntegerField()
    salary = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, default=1)



class Applicant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)



