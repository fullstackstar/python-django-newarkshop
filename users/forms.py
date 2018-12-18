from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfileInfo, UserPaymentInfo
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email Address', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'loginput'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(label='password*', widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='Confirm Password*', required=True, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'confirm_password', 'email')
        widgets = {
            'username': forms.EmailInput(attrs={
                'placeholder': 'Email',
            }),
            'email': forms.HiddenInput,
        }
        labels = {
            'username': 'Email Address'
            # "other_field": "Other Title"
        }
        error_messages = {
            'username': {
                'unique': "A user with that EmailAddress already exists.",
            }
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if len(password) < 10:
            self.add_error('password', "Password length must be greater than 10")
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
    business_name = forms.CharField(label='Business_name*', max_length=100)
    first_name = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label='', max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    address_line1 = forms.CharField(
        label='Business Address*', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line1'})
    )
    address_line2 = forms.CharField(
        label='', max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line2'})
    )
    city = forms.CharField(
        label='', max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    st = forms.CharField(
        label='', max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ST'})
    )
    zip_code = forms.CharField(
        label='', max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ZIP Code'})
    )
    phone_number = forms.CharField(
        label='', max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone 222-222-2222'})
    )
    of_employees = forms.BooleanField(
        label='# of Employees(Optional)', required=False,
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = UserProfileInfo
        fields = (
            'business_name', 'first_name', 'last_name', 'address_line1',
            'address_line2', 'city', 'st', 'zip_code', 'phone_number', 'of_employees'
        )


class UserPaymentInfoForm(forms.ModelForm):
    card_number = forms.CharField(
        label='Credit Card', max_length=19,
        widget=forms.TextInput()
    )
    exp_date = forms.DateField(
        label='Expiration', required=True,
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
