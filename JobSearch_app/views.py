from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages  # Added import statement
from .models import *  # Added import statement
from django.contrib.auth.decorators import login_required


@login_required
def profileView(request):
    user = request.user
    if request.method == 'POST':
        user.birth_date = request.POST.get('birth_date')
        user.specialty = request.POST.get('specialty')
        user.experience = request.POST.get('experience')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('home_url')  # Redirect to home or any other page after saving
    return render(request, 'profile_template.html', {'user': user})
def homeView(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home_template.html', context)


def vacanciesView(request):
    # Fetch all vacancies from the database
    vacancies = Vacancy.objects.all()

    # Pass the vacancies to the template
    context = {'vacancies': vacancies}
    return render(request, 'vacancies.html', context)


def vacancyDetail(request, vacancy_id):
    if request.method == 'GET':
        # Получаем объект вакансии по идентификатору
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

        # Передаем объект вакансии в шаблон и рендерим страницу
        return render(request, 'vacancy_detail.html', {'vacancy': vacancy})

    elif request.method == 'POST':
        # Retrieve the logged-in user
        user = request.user

        # Retrieve the vacancy
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            messages.error(request, 'Vacancy not found.')
            return redirect('vacancies_url')

        # Create an application
        applicant = Applicant(user=user, vacancy=vacancy, status='Applied')
        applicant.save()

        messages.success(request, 'Application submitted successfully.')
        return redirect('vacancies_url')  # Redirect to vacancies page or any other page

    else:
        messages.error(request, 'Invalid request method.')
        return redirect('vacancies_url')  # Redirect to vacancies page or any other page



def createVacancyView(request):
    if request.method == 'GET':
        return render(request, 'create_vacancy_template.html')
    elif request.method == 'POST':
        title = request.POST.get('title_input')
        expyear = request.POST.get('expyear')
        salary = request.POST.get('salary')
        description_input = request.POST.get('description_input')
        user = request.user

        if user is not None:
            # Create a new instance of Vacancy model
            new_vacancy = Vacancy.objects.create(
                title=title,
                description=description_input,
                company=user,  # Assuming the user is the company
                expyear=expyear,
                salary=salary
            )
            # Optionally, you can add a success message
            messages.success(request, 'Vacancy created successfully.')
            return redirect('home_url')
        else:
            messages.error(request, 'Invalid you')
            return redirect('home_url')

def logOutView(request):
    logout(request)
    return redirect('home_url')

def logInView(request):
    if request.method == 'GET':
        return render(request, 'login_template.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login_url')

def registerView(request):
    if request.method == 'GET':
        return render(request, 'registration_template.html')
    elif request.method == 'POST':
        input_email = request.POST.get('email')
        input_pass1 = request.POST.get('password1')
        input_pass2 = request.POST.get('password2')
        this_user = CustomUser.objects.filter(email=input_email)
        if this_user.exists():
            context = {
                'message': 'This email is already taken!'
            }
            return render(request, 'registration_template.html', context=context)
        if input_pass1 != input_pass2:
            context = {
                'message': 'Passwords don`t match!',
                'email': input_email
            }
            return render(request, 'registration_template.html', context=context)

        user = CustomUser.objects.create_user(email=input_email, password=input_pass1)
        login(request, user)
        return redirect('home_url')

def registerCompanyView(request):
    if request.method == 'GET':
        return render(request, 'registration_company_template.html')
    elif request.method == 'POST':
        input_email = request.POST.get('email')
        input_pass1 = request.POST.get('password1')
        input_pass2 = request.POST.get('password2')
        companyName = request.POST.get('company_name')
        companyAddress = request.POST.get('company_address')
        companyIndustry = request.POST.get('industry')

        this_user = CustomUser.objects.filter(email=input_email)
        if this_user.exists():
            context = {
                'message': 'This email is already taken!'
            }
            return render(request, 'registration_company_template.html', context=context)
        if input_pass1 != input_pass2:
            context = {
                'message': 'Passwords don`t match!',
                'email': input_email
            }
            return render(request, 'registration_company_template.html', context=context)

        user = CustomUser.objects.create_user(
            email=input_email,
            password=input_pass1,
            is_company=True,
            company_name=companyName,
            company_address=companyAddress,
            industry=companyIndustry
        )
        login(request, user)
        return redirect('home_url')
