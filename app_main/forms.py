from django import forms


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
    firstname = forms.CharField(
        label="First name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    lastname = forms.CharField(
        label="Last name:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
