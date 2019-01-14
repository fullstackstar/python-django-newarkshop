from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import UserProfileInfo, UserPaymentInfo
from .models import CustomUser

import re


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email Address', max_length=30,
        widget=forms.TextInput(attrs={'class': 'loginput'})
    )


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password*', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password*', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        widgets = {
            'username': forms.EmailInput(attrs={
                'placeholder': 'Email',
            }),
            'email': forms.HiddenInput,
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
            }),
        }
        labels = {
            'username': 'Email Address',
            "first_name": '',
            "last_name": '',
        }
        help_texts = {
            'username': ''
        }
        error_messages = {
            'username': {
                'unique': "A user with that EmailAddress already exists.",
            }
        }

        fields = (
            'username', 'password', 'confirm_password', 'email',
            'first_name', 'last_name'
        )

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password is not None and confirm_password is not None:
            if not is_valid(password, pattern):
                self.add_error('password', "Password must contain: 8Characters l letter 1 number")
            if password != confirm_password:
                self.add_error('confirm_password', "Password does not match")

        return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(False)
    #     user.email = user.username
    #     user = super().save()
    #
    #     return user


class UserProfileInfoForm(forms.ModelForm):
    business_name = forms.CharField(
        label='Business Name*', max_length=100,
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    address_line_one = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line1'})
    )
    address_line_two = forms.CharField(
        label='', max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line2'})
    )
    city = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    st = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'ST'})
    )
    zip_code = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Zip Code'})
    )
    phone_number = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Phone 222-222-2222'})
    )
    of_employees = forms.CharField(
        label='# of Employees(Optional)', max_length=50, required=False,
        widget=forms.TextInput()
    )
    company = forms.CharField(
        label='Company*', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': ''})
    )

    class Meta:
        model = UserProfileInfo
        fields = (
            'business_name', 'address_line_one',
            'address_line_two', 'city', 'st', 'zip_code', 'phone_number',
            'of_employees', 'company'
        )

    def clean(self):
        cleaned_data = super(UserProfileInfoForm, self).clean()

        pattern = '(?:\(\d{3}\)|\d{3}-)\d{3}-\d{4}$'

        phone_number = cleaned_data.get('phone_number')

        if not is_valid(phone_number, pattern):
            self.add_error('phone_number', 'phone_number format is not correct')

        users = UserProfileInfo.objects.filter(phone_number=phone_number)
        if users.count() > 0:
            self.add_error('phone_number', 'phone_number is already exist')

        return cleaned_data


class UserPaymentInfoForm(forms.ModelForm):
    card_number = forms.CharField(
        label='Credit Card',
        widget=forms.TextInput(attrs={'placeholder': '4242-4242-4242-4242'})
    )
    exp_date = forms.DateField(
        label='Expiration',
        widget=forms.TextInput(attrs={'type': 'date', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        label='cvv', max_length=10,
        widget=forms.TextInput(attrs={'type': 'number'})
    )

    class Meta:
        model = UserPaymentInfo
        fields = (
            'card_number', 'exp_date', 'cvv'
        )

    def clean(self):
        cleaned_data = super(UserPaymentInfoForm, self).clean()

        pattern = '\d{4}-\d{4}-\d{4}-\d{4}'

        card_number = cleaned_data.get("card_number")

        if not is_valid(card_number, pattern):
            self.add_error('card_number', "card_number format is not correct")

        return cleaned_data


def is_valid(sequence, pattern):
    """Returns `True' if the sequence is a valid credit card number.

    A valid credit card number
    - must contain exactly 16 digits,
    - must start with a 4, 5 or 6
    - must only consist of digits (0-9) or hyphens '-',
    - may have digits in groups of 4, separated by one hyphen "-".
    - must NOT use any other separator like ' ' , '_',
    - must NOT have 4 or more consecutive repeated digits.
    """

    match = re.match(pattern, sequence)

    if match is None:
        return False

    return True
