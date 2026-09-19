import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, normalize_phone_number




class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["phone_number", "full_name"]

    def clean_phone_number(self):
        phone_number = normalize_phone_number(self.cleaned_data["phone_number"])

        if not re.match(r"^\+234\d{10}$", phone_number):
            raise forms.ValidationError("Enter a valid Nigerian phone number.")

        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("An account with this phone number already exists.")

        return phone_number
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Phone number")
    
class AccountEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]