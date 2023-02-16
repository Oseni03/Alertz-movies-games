from .forms import UserLoginForm, RegistrationForm, UserEditForm

def account(request):
    context = {
        "reg_form": RegistrationForm(),
        "login_form": UserLoginForm(),
    }
    if request.user.is_authenticated:
        context["update_form"] = UserEditForm(instance=request.user)
    return context