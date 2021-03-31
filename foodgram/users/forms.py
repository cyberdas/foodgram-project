from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from recipes.tasks import send_verification_email

from .models import User


class CreationForm(UserCreationForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Данный email уже занят")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            auth_user = authenticate(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password1"]
            )
            login(self.request, auth_user)
            send_verification_email.delay(user.id)
        return user
