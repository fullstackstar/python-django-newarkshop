from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    line_number = amount = forms.CharField(
        label='Line Number',
        widget=forms.TextInput(attrs={'type': 'number'})
    )
    amount = forms.CharField(
        label='Amount',
        widget=forms.TextInput(attrs={'type': 'number'})
    )

    class Meta:
        model = Transaction
        fields = ('line_number', 'amount')

    def clean(self):
        cleaned_data = super(TransactionForm, self).clean()

        return cleaned_data
