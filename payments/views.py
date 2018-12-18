from django.shortcuts import render
from django.views.generic.base import TemplateView

class PaymentPageView(TemplateView):
    template_name = 'payments/home.html'
