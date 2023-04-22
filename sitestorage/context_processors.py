from sitestorage.forms import UserAuthorizationForm, UserRegistrationForm


def login_form(request):
    user_registration_form = UserRegistrationForm()
    user_login_form = UserAuthorizationForm()

    return {
        'user_registration_form': user_registration_form,
        'user_login_form': user_login_form
    }
