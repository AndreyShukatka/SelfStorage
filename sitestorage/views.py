import datetime
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView
from .forms import PaymentForm, UserProfileForm, UserRegistrationForm, UserAuthorizationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from yookassa import Payment

from .models import Order, PaymentOrder, Storage, User


class Index(View):
    template_name = 'sitestorage/index.html'

    def get_context_data(self):
        storage = Storage.objects.order_by('?')[0]
        storage_quantity = storage.address.get_storage_quantity()
        storage_occupied = storage.address.occupied
        context = {
            'title': 'Self Storage',
            'storage': {
                'pk': storage.pk,
                'photo': storage.photo.url,
                'address': storage.address,
                'temperature': storage.temperature,
                'avaible': storage_quantity - storage_occupied,
                'quantity': storage_quantity,
                'height': storage.height,
                'price': storage.price
            }
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

def pay(request, pk):
    storage_obj = get_object_or_404(Storage, pk=pk)
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        card_year = f"20{payment_form.data['card_year']}"
        card_month = payment_form.data['card_month']
        card_holder = payment_form.data['card_holder']
        cvc = payment_form.data['card_cvc']
        if payment_form.is_valid():
            form = payment_form.save(commit=False)
            card_number = form.card_number
            form.card_number = form.card_number[-4:]
            form.storage = storage_obj
            cost = storage_obj.price
            payment_payload = {
                "amount": {
                    "value": str(cost),
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": "bank_card",
                    "card": {
                        "cardholder": card_holder,
                        "csc": cvc,
                        "expiry_month": card_month,
                        "expiry_year": card_year,
                        "number": card_number
                    }
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri(reverse('confirm_pay', kwargs={'pk': pk}))
                },
                "description": form.storage
            }
            payment = Payment.create(payment_payload)

            payment_confirmation = payment.confirmation.confirmation_url
            payment_id = payment.id
            form.payment_id = payment_id

            form.save()

            return HttpResponseRedirect(payment_confirmation)
    else:
        payment_form = PaymentForm()
    context = {
        'storage_pk': storage_obj.pk,
        'payment_form': payment_form
    }
    return render(request, 'sitestorage/pay.html', context)

def confirm_pay(request, pk):
    storage_obj = get_object_or_404(Storage, pk=pk)
    cost = storage_obj.price
    payment = PaymentOrder.objects.filter(storage=storage_obj).first()
    payment_id = payment.payment_id
    idempotence_key = str(uuid.uuid4())
    response = Payment.capture(
        payment_id,
        {
            "amount": {
                "value": cost,
                "currency": "RUB"
            }
        },
        idempotence_key
    )
    if response.status == 'succeeded':
        payment.status = PaymentOrder.SUCCESS
        order_obj = Order.objects.create(
            user=request.user,
            storage=storage_obj,
            reception_conditions='sm',
            delivery_conditions='sm',
            reception_date=datetime.datetime.now(),
            paid_to=datetime.datetime.now() + datetime.timedelta(days=30)
        )
        payment.order = order_obj
        payment.save()

    return HttpResponseRedirect(reverse('index'))

def get_modal_window(request):
    return HttpResponse("<script> document.getElementById('Entrance').click()</script>")
