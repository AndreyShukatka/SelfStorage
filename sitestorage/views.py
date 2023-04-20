from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserAuthorizationForm
from django.contrib.auth import authenticate, login
from .models import User


def index(request):
    user_registration_form = UserRegistrationForm()
    user_login_form = UserAuthorizationForm()
    context = {
        'user_registration_form': user_registration_form,
        'user_login_form': user_login_form
    }
    registration(request)
    authorize(request)
    return render(request, 'index.html', context=context)


def boxes(request):
    user_registration_form = UserRegistrationForm()
    context = {
        'user_registration_form': user_registration_form
    }
    registration(request)
    return render(request, 'boxes.html', context=context)


def faq(request):
    user_registration_form = UserRegistrationForm()
    context = {
        'user_registration_form': user_registration_form
    }
    registration(request)
    return render(request, 'faq.html', context=context)


def my_rent(request):
    if request.POST:
        response = request.POST
        user = User.objects.get(id=request.user.id)
        email = response.get('EMAIL_EDIT')
        phone = response.get('PHONE_EDIT')
        user.email, user.phone = email, phone
        user.save()
    return render(request, 'my-rent.html')


def registration(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'registration':
            user_registration_form = UserRegistrationForm(request.POST)
            if user_registration_form.is_valid():
                new_user = user_registration_form.save(commit=False)
                new_user.set_password(user_registration_form.cleaned_data['password'])
                new_user.save()
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(email=email, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
    else:
        pass


def authorize(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
