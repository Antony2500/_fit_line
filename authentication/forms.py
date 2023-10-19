from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.urls import reverse_lazy


# Class of the user login form / Клас форми для входу користувача
from django import forms
from django.contrib.auth import authenticate

# ...


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter your username", "required": True}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "required": True}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            raise forms.ValidationError("Please enter your username.")
        if not password:
            raise forms.ValidationError("Please enter your password.")

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        # Check if the user exists and the password is correct
        if user is None or not user.check_password(password):
            raise forms.ValidationError("Invalid username or password.")

        # Return cleaned data if everything is valid
        return cleaned_data


# Class for creating a user registration form(клас для створення форми реєстрації користувача)
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the email field as required (Встановлює поле електронної пошти як обов'язкове)
        self.fields['email'].required = True

        # Apply the "form-input" class to visible form fields (Застосовує клас "form-input" до видимих полів форми)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-input'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if a user with this email already exists (Перевіряє, чи вже існує користувач з такою електронною поштою)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")  # Ця електронна пошта вже використовується

        return email


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(
        attrs={'autofocus': 'True', 'autocomplete': 'current-password', 'class': 'form-control'}))

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем атрибут "success_url" для указания URL, на который перенаправлять после успешного изменения пароля
        self.success_url = reverse_lazy('successfully-completed')


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
