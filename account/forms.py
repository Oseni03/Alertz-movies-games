from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    PasswordChangeForm,
)

from .models import Customer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"autocorrect": "off", "autocapitalize": "off"}),
    )
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Enter name", min_length=4, max_length=50, help_text="Required"
    )
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, required=True
    )
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput, required=True
    )

    class Meta:
        model = Customer
        fields = ("username", "first_name", "last_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match")
        return cd["password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        r = Customer.objects.filter(email=email)
        if r.exists():
            raise forms.ValidationError(
                "Please choose another email, that's already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Username",
            }
        )
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "First Name",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label="Enter name", min_length=4, max_length=50, help_text="Required"
    )
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )

    class Meta:
        model = Customer
        fields = ("username", "first_name", "last_name", "email")

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     r = Customer.objects.filter(email=email)
    #     if r.exists():
    #         raise forms.ValidationError(
    #             "Please choose another email, that's already taken"
    #         )
    #     return email



class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput())

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = Customer.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                "Unfortunately we could not find that email address"
            )
        return email


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Old Password",
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New Password",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        )
    )

    class Meta:
        model = Customer
        fields = (
            "password1",
            "password2",
        )
