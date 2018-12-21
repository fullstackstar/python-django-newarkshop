import stripe

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render

from users.models import CustomUser, UserPaymentInfo

stripe.api_key = settings.STRIPE_SECRET_KEY


# class PaymentPageView(TemplateView):
#     template_name = 'payments/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['key'] = settings.STRIPE_PUBLISHABLE_KEY
#         return context
def home(request):
    pay_info = UserPaymentInfo.objects.get(user_id=request.user.id)
    amount_dollar = int(pay_info.pay_amount)
    amount_cent = amount_dollar * 100
    context = {
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'amount_dollar': amount_dollar,
        'amount_cent': amount_cent
    }
    return render(request, 'payments/home.html', context)


def charge(request):
    pay_info = UserPaymentInfo.objects.get(user_id=request.user.id)
    amount_dollar = int(pay_info.pay_amount)
    amount_cent = amount_dollar * 100

    if request.method == 'POST':
        charge = stripe.Charge.create(
            # amount=500,
            amount=amount_cent,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        context = {'amount_dollar': amount_dollar}
        return render(request, 'payments/charge.html', context)
