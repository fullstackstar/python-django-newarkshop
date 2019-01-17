from django import forms
from .models import Transaction
from users.models import UserProfileInfo
import re


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(
        label='', max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Phone 222-222-2222'})
    )

    def clean(self):
        cleaned_data = super(PhoneVerificationForm, self).clean()

        pattern = '(?:\(\d{3}\)|\d{3}-)\d{3}-\d{4}$'

        phone_number = cleaned_data.get('phone_number')

        if not is_valid(phone_number, pattern):
            self.add_error('phone_number', 'phone_number is not correct')

        users = UserProfileInfo.objects.filter(phone_number=phone_number)
        if not users.count():
            self.add_error('phone_number', 'Consumer with that number does not exist. Check your phone number.')

        return cleaned_data


class TransactionForm(forms.ModelForm):
    amount = forms.CharField(
        label='Transaction Amount',
        widget=forms.TextInput(attrs={'placeholder': 'Transaction Amount'})
    )

    class Meta:
        model = Transaction
        fields = ('amount',)

    def clean(self):
        cleaned_data = super(TransactionForm, self).clean()

        return cleaned_data


class EmailSearchForm(forms.Form):
    email = forms.CharField(
        label='Email', max_length=50,
        widget=forms.TextInput(attrs={'type': 'email'})
    )

    def clean(self):
        cleaned_data = super(EmailSearchForm, self).clean()

        return cleaned_data


def is_valid(sequence, pattern):
    match = re.match(pattern, sequence)

    if match is None:
        return False

    return True
