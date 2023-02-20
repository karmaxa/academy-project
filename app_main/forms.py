from django import forms

from app_main.helpers import get_all_teachers_as_choices
from app_main.helpers import roles


class LogInForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class NewUserForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    firstname = forms.CharField(
        label="First name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    lastname = forms.CharField(
        label="Last name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    role = forms.ChoiceField(
        label="Role:",
        choices=roles,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    firstname = forms.CharField(
        label="First name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    lastname = forms.CharField(
        label="Last name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class NewClassRoomForm(forms.Form):
    name = forms.CharField(
        label="Name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    teacher = forms.ChoiceField(
        label="Teacher:",
        choices=get_all_teachers_as_choices,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )
