from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages  # Added import statement
from .models import CustomUser  # Added import statement
def homeView(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home_template.html', context)

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
        input_pass1 = request.POST.get('pass1')
        input_pass2 = request.POST.get('pass2')
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
