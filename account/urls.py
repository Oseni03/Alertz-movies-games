from django.urls import path
from django.views import generic
from django.contrib.auth import views as auth_views

from . import views 
from .decorators import anonymous_required
from .forms import UserLoginForm, PwdResetForm

app_name = "account"

urlpatterns = [
  path("register/", anonymous_required(views.RegistrationFormView.as_view()), name="register"),
  path("activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"),
  path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
  path("login/", anonymous_required(views.MyLoginView.as_view()), name="login"),
  # path("login/", auth_views.LoginView.as_view(
  #   template_name="account/login.html", 
  #   form_class=UserLoginForm), name="login"),
  path("password-reset/", auth_views.PasswordResetView.as_view(
    template_name="account/password_reset_form.html",
    success_url = "/account/reset-password-sent/",
    email_template_name='account/email/password_reset_email.html',
    form_class=PwdResetForm,
    ), name="password-reset"),
    
  path('password_reset_confirm/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
      template_name="account/password_reset_confirm.html",
      success_url="/account/password-reset-complete/"), 
      name="password_reset_confirm"),
  
  path('reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
      template_name="account/password_reset_sent.html"), 
      name="password_reset_done"),
    
  path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
      template_name="account/password_reset_complete.html"),
      name="password_reset_complete"),
    
  # USER DASHBOARD
  path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
  path("profile/edit/", views.user_update, name="edit_detail"),
  path("profile/delete-confirm/", generic.TemplateView.as_view(template_name="account/delete_confirm.html"), name="delete_confirm"),
]