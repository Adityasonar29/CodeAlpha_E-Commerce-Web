from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Product


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image_url', 'featured', 'brand', 'category']


class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(required=True, help_text="Required. Enter your last name.")
    email = forms.EmailField(required=True, help_text="Required. A valid email address.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_classes = 'mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none focus:border-indigo-400 focus:ring-0'
        for field in self.fields.values():
            field.widget.attrs.update({'class': field_classes})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()

        if "@" not in email:
            raise ValidationError("Please enter a valid email address.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists.")

        return email
