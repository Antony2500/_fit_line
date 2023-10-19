import phonenumbers

from django import forms
from django.core.validators import EmailValidator

from .models import Customer, Order


class CustomerProfileForm(forms.ModelForm):
    mobile = forms.CharField(
        label='Mobile',
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Починайте +380..', 'inputmode': 'numeric'}),
        initial='+380',
        max_length=13,
        min_length=13,
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'you@example.com'}),
        validators=[EmailValidator(message='Введіть коректну адресу електронної пошти.')]
    )

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        # Проверяем, что номер начинается с "+380" и состоит из 13 символов (включая "+")
        if not mobile.startswith('+380') or not mobile[1:].isdigit() or len(mobile) != 13:
            raise forms.ValidationError(
                'Введіть коректний номер телефону (починається з +380 і складається з 13 символів)')

        return mobile

    def clean(self):
        super().clean()

        # Можете оставить эту проверку, но измените на поле формы email, а не self.cleaned_data['email']
        if not self.cleaned_data['email']:
            raise forms.ValidationError("Введіть коректну адресу електронної пошти.")

        return self.cleaned_data

    class Meta:
        model = Customer
        fields = ['name', 'surname', 'email', 'mobile', 'state', 'city',
                  'branch_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-group'}),
            'surname': forms.TextInput(attrs={'class': 'form-group'}),
            'state': forms.Select(attrs={'class': 'form-group', 'placeholder': 'Виберіть область'}),
            'city': forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Введіть назву ...'}),
            'branch_number': forms.TextInput(attrs={'class': 'form-group',
                                                    'placeholder': 'Введіть номер відділення (НП)'}),
        }


class DeliveryMethod(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordering_method', 'comment']
        widgets = {
            'ordering_method': forms.Select(attrs={'class': 'form-group', 'placeholder': 'Виберіть спосіб'}),
            'comment': forms.Textarea(attrs={'class': 'form-group', 'placeholder': 'Введіть свої побажання або питання перед покупкою'}),
        }
