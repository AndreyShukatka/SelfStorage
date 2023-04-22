from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView
from .forms import UserProfileForm, UserRegistrationForm, UserAuthorizationForm
from django.contrib.auth import authenticate, login
from .models import Storage, User
from django.contrib.auth.hashers import make_password


class Index(View):
    template_name = 'sitestorage/index.html'

    def get_context_data(self):
        storage = Storage.objects.order_by('?')[0]
        context = {
            'title': 'Self Storage',
            'storage': storage
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
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
        if request.POST.get('type') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        context = self.get_context_data()

        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('modal')
    template_name = 'sitestorage/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        if self.request.user.is_anonymous:
            return None
        return self.request.user

    def post(self, request):
        user = self.request.user
        password_old = user.password
        password_new = request.POST.get('PASSWORD_EDIT')
        email = request.POST.get('EMAIL_EDIT')
        phone = request.POST.get('PHONE_EDIT')
        username = request.POST.get('NAME_EDIT')
        user.email, user.phone, user.username = email, phone, username
        if password_new != password_old:
            password_new = make_password(request.POST.get('PASSWORD_EDIT'))
            print(password_new)
            user.password = password_new
        user.save()
        return redirect('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse('modal'))
        return super().get(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class UserLoginView(View):
    def post(self, request, *args: str, **kwargs) -> HttpResponse:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        form = UserAuthorizationForm
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')


class BoxesListView(ListView):
    model = Storage
    template_name = 'sitestorage/boxes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Boxes'
        return context

    def post(self, request, *args, **kwargs):
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
        if request.POST.get('type') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        context = {
            'title': 'Self Storage'
        }

        return render(request, self.template_name, context)

class FaqView(View):
    template_name = 'sitestorage/faq.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'FAQ'
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
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
        if request.POST.get('type') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        context = {
            'title': 'Self Storage'
        }

        return render(request, self.template_name, context)


def get_modal_window(request):
    return HttpResponse("<script> document.getElementById('Entrance').click()</script>")
