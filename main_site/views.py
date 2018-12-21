from django.shortcuts import render, redirect
from users.models import UserProfileInfo
from django.contrib.auth.decorators import login_required

from users.models import CustomUser
from .models import Transaction
from .forms import TransactionForm

import datetime


def index(request):
    """The home page for Newark Shop."""
    user = request.user
    if user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'vendor':
            return redirect('main_site:vendor_dashboard')
        if user_type == 'consumer':
            return redirect('main_site:consumer_dashboard')

    return render(request, 'main_site/index.html')


@login_required
def vendor_dashboard(request):
    transactions = Transaction.objects.filter(vendor_id=request.user.id)

    context = {'transactions': transactions}
    return render(request, 'main_site/vendor_dashboard.html', context)


@login_required
def vendor_transactions(request):
    transactions = Transaction.objects.select_related('consumer__userprofileinfo').filter(vendor_id=request.user.id)
    context = {'transactions': transactions}
    return render(request, 'main_site/vendor_transactions.html', context)


@login_required
def consumer_dashboard(request):
    transactions = Transaction.objects.filter(consumer_id=request.user.id)
    context = {'transactions': transactions}

    return render(request, 'main_site/consumer_dashboard.html', context)


@login_required
def vendors(request):
    # vendors = UserProfileInfo.objects.filter(user_type='consumer')
    vendor_users = CustomUser.objects.filter(user_type='vendor')
    context = {'vendor_users': vendor_users}
    return render(request, 'main_site/vendors.html', context)


@login_required
def vendor(request, vendor_id):
    vendor_user = CustomUser.objects.get(id=vendor_id)
    consumer_user = CustomUser.objects.get(id=request.user.id)

    if request.method != 'POST':
        transaction_form = TransactionForm()
    else:
        transaction_form = TransactionForm(data=request.POST)

        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # transaction.business_name = business_name
            transaction.vendor = vendor_user
            transaction.consumer = consumer_user
            transaction.consumer_status = 'Purchased'
            transaction.save()

            return redirect('main_site:consumer_vendors')

    context = {'vendor_user': vendor_user, 'transaction_form': transaction_form}
    return render(request, 'main_site/vendor.html', context)


def vendor_accept(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.vendor_status = 'Accepted'
    transaction.accepted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    transaction.save()

    return redirect('main_site:vendor_transactions')
