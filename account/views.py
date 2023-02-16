from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm, UserEditForm, UserLoginForm
from .tokens import account_activation_token
from .models import Customer


# Create your views here.
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/new_dash.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        context["movies"] = self.request.user.movies.prefetch_related("region", "genres", "date").all()[:5]
        context["games"] = self.request.user.games.prefetch_related("platforms", "genres", "date").all()[:5]
        return context 
    
    # def get(self, request, *args, **kwargs):
    #     if not request.user.subscription:
    #         return redirect("alert:checkout")
    #     super().get(request, *args, **kwargs)


class MyLoginView(LoginView):
    template_name = "account/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(self.request, user)
                    messages.success(self.request, "login succesful")
                    return redirect(reverse("account:dashboard"))
                else:
                    messages.info(
                        self.request,
                        "Account not verified. Please check your email to verify your account!",
                    )
            else:
                messages.info(
                    self.request,
                    "Invalid login details",
                )
        return super().form_valid(form)
    

class RegistrationFormView(generic.FormView):
    template_name = "account/register.html"
    form_class = RegistrationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.email = form.cleaned_data["email"]
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = "Activate your Account"
        message = render_to_string(
            "account/email/account_activation.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        user.email_user(subject, message)

        messages.success(
            self.request,
            "Account created successfully. Verify your email to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.info(self.request, error)
        return super().form_invalid(form)
    

@login_required
@require_POST
def user_update(request):
    # form = UserEditForm(instance=request.user)
    if request.POST:
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
        else:
            for error in form.errors:
                messages.info(request, error)
    return redirect(request.META["HTTP_REFERER"])
    # return render(request, "account/edit_detail.html", {"form": form})


def account_activate(request, uidb64, token):
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(id=id)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Account confirmation successful")
        return redirect("account:dashboard")
    else:
        return render(request, "account/activation_invalid.html")

