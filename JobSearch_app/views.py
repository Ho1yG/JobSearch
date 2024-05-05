from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages  # Added import statement
from .models import *  # Added import statement
from django.contrib.auth.decorators import login_required




def delete_applicant_view(request, applicant_id):

    applicant = get_object_or_404(Applicant, id=applicant_id)

    applicant.delete()
    return redirect('home_url')


def applicant_detail_view(request, applicant_id):
    # Retrieve the applicant object
    applicant = get_object_or_404(Applicant, id=applicant_id)

    # Pass the applicant object to the template
    context = {'applicant': applicant}
    return render(request, 'applicant_detail.html', context)

@login_required
def aplicantsView(request):
    # Retrieve all applicants related to the current user
    user_applicants = Applicant.objects.filter(user=request.user)

    # Pass the list of applicants to the template
    context = {'applicants': user_applicants}
    return render(request, 'applicants_template.html', context)

@login_required
def delete_user_view(request):
    # Retrieve the user object
    user = request.user

    user.delete()
    return redirect('home_url')

@login_required
def change_application_status_view(request, applicant_id):
    if request.method == 'GET':
        # Get the applicant object
        applicant = get_object_or_404(Applicant, id=applicant_id)

        # Get the new status from the query parameters
        new_status = request.GET.get('status')

        if new_status:
            # Update the applicant's status
            applicant.status = new_status
            applicant.save()

        # Redirect back to the vacancy page
        return redirect('view_vacancy_url', vacancy_id=applicant.vacancy.id)
    else:
        # If the request method is not GET, handle it accordingly
        return redirect('error_url')
@login_required
def viewUserVacancyView(request, applicant_id):
    applicant = get_object_or_404(Applicant, id=applicant_id)

    context = {'applicant': applicant}
    return render(request, 'vacancy_user_template.html', context)


@login_required
def viewVacancyView(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    context = {'vacancy': vacancy}
    return render(request, 'vacancy_company_template.html', context)

@login_required
def deleteVacancyView(request, vacancy_id):
    # Получаем объект вакансии или возвращаем 404 ошибку, если он не найден
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    # Проверяем, принадлежит ли вакансия текущей компании
    if vacancy.company == request.user:
        # Удаляем вакансию
        vacancy.delete()
        # Перенаправляем на страницу профиля компании с сообщением об успешном удалении
        messages.success(request, 'Vacancy deleted successfully.')
        return redirect('company_profile_url')
    else:
        # Если вакансия не принадлежит текущей компании, перенаправляем на страницу ошибки
        messages.error(request, 'You do not have permission to delete this vacancy.')
        return redirect('company_profile_url')  # или на другую страницу


def updateVacancyView(request, vacancy_id):
    # Получаем объект вакансии или возвращаем 404 ошибку, если он не найден
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    # Проверяем, принадлежит ли вакансия текущей компании
    if vacancy.company == request.user:
        if request.method == 'POST':
            # Обработка POST-запроса для обновления вакансии
            vacancy.title = request.POST.get('title_input')
            vacancy.expyear = request.POST.get('expyear')
            vacancy.salary = request.POST.get('salary')
            vacancy.description = request.POST.get('description_input')

            # Обновляем категорию и тип работы
            vacancy.category = Category.objects.get(id=request.POST.get('category_select'))
            vacancy.work_type = WorkType.objects.get(id=request.POST.get('worktype_select'))

            vacancy.save()
            messages.success(request, 'Vacancy updated successfully.')
            return redirect('company_profile_url')
        else:
            # Получаем все категории и типы работы из базы данных
            categories = Category.objects.all()
            worktypes = WorkType.objects.all()

            # Передаем их в контекст шаблона
            context = {
                'vacancy': vacancy,
                'categories': categories,
                'worktypes': worktypes
            }
            # Отображаем форму для обновления вакансии
            return render(request, 'update_vacancy_template.html', context)
    else:
        # Если вакансия не принадлежит текущей компании, перенаправляем на страницу ошибки
        messages.error(request, 'You do not have permission to update this vacancy.')
        return redirect('company_profile_url')  # или на другую страницу
@login_required
def companyProfileView(request):
    company = request.user
    if request.method == 'POST':
        # Обработка POST-запроса для изменения информации о компании
        company.company_name = request.POST.get('company_name')
        company.company_address = request.POST.get('company_address')
        company.industry = request.POST.get('industry')
        company.save()
        messages.success(request, 'Company profile updated successfully.')
        return redirect('home_url')  # Перенаправление на главную страницу или другую страницу

    return render(request, 'company_profile_template.html', {'company': company})


@login_required
def profileView(request):
    user = request.user
    if request.method == 'POST':
        user.birth_date = request.POST.get('birth_date')
        user.specialty = request.POST.get('specialty')
        user.experience = request.POST.get('experience')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.description = request.POST.get('description')
        user.save()
        return redirect('home_url')  # Redirect to home or any other page after saving
    return render(request, 'profile_template.html', {'user': user})
def homeView(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home_template.html', context)


def vacanciesView(request):
    # Получаем значение поискового запроса из параметра GET
    search_query = request.GET.get('search')

    # Если есть поисковой запрос, фильтруем вакансии по названию
    if search_query:
        vacancies = Vacancy.objects.filter(title__icontains=search_query)
    else:
        # Если поискового запроса нет, выводим все вакансии
        vacancies = Vacancy.objects.all()

    # Получаем список всех категорий для фильтрации
    categories = Category.objects.all()

    # Проверяем, была ли отправлена форма с фильтрами
    if 'category' in request.GET:
        selected_categories = request.GET.getlist('category')
        # Фильтруем вакансии по выбранным категориям
        vacancies = vacancies.filter(category__id__in=selected_categories)

    return render(request, 'vacancies.html', {'vacancies': vacancies, 'categories': categories})

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


@login_required
def createVacancyView(request):
    if request.method == 'POST':
        title = request.POST.get('title_input')
        expyear = request.POST.get('expyear')
        salary = request.POST.get('salary')
        description_input = request.POST.get('description_input')
        category_id = request.POST.get('category')
        worktype_id = request.POST.get('worktype')

        if title and expyear and salary and description_input and category_id and worktype_id:
            category = Category.objects.get(id=category_id)
            worktype = WorkType.objects.get(id=worktype_id)
            company_id = request.user.id  # Предполагается, что компания пользователя является текущим пользователем
            vacancy = Vacancy.objects.create(title=title, expyear=expyear, salary=salary, description=description_input, category=category, work_type=worktype, company_id=company_id)
            vacancy.save()
            messages.success(request, 'Vacancy created successfully.')
            return redirect('home_url')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('create_vacancy_url')
    else:
        categories = Category.objects.all()
        worktypes = WorkType.objects.all()
        return render(request, 'create_vacancy_template.html', {'categories': categories, 'worktypes': worktypes})

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
