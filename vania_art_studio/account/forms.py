from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from vania_art_studio.account.models import Profile
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from cloudinary.forms import CloudinaryInput

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = 'Потребителско име'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Парола'
        self.fields['password2'].widget.attrs['placeholder'] = 'Потвърди парола'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Паролите не съвпадат!')
        if len(password1) < 8:
            raise ValidationError('Паролата трябва да е минимум 8 символа')
        if password1.isalpha():
            raise ValidationError('Паролата трябва да съдържа и цифри')
        if password2.isdigit():
            raise ValidationError('Паролата трябва да съдържа и букви')

        return password2


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Грешно потребителско име или парола'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Потребителско име'
        self.fields['password'].widget.attrs['placeholder'] = 'Парола'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'age', 'city', 'profile_picture')
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'age': 'Възраст',
            'city': 'Град',
            'profile_picture': 'Профилна снимка'
        }
