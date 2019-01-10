from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.models import CustomUser
from .models import Transaction
from .forms import TransactionForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def index(request):
    """The home page for Newark Shop."""
    user = request.user
    if user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'vendor':
            return redirect('main_site:vendor_dashboard')
        if user_type == 'consumer':
            return redirect('main_site:consumer_dashboard')

    # send_mail('Hello', 'password reset test', 'NewarkShop <postmaster@sandbox06f5ad68577b4b298c00df0f028d5a7b.mailgun.org>', ['sweetnougat@mail.com'])
    # EmailMultiAlternatives('Hello', 'password reset test', 'NewarkShop <postmaster@sandbox06f5ad68577b4b298c00df0f028d5a7b.mailgun.org>', ['sweetnougat@mail.com']).send()

    return render(request, 'main_site/index.html')


@login_required
def vendor_dashboard(request):
    transactions_list = Transaction.objects.filter(vendor_id=request.user.id)
    transactions = get_pagenatied_items(request, transactions_list)

    context = {'transactions': transactions['data'], 'count': transactions['count']}
    return render(request, 'main_site/vendor_dashboard.html', context)


@login_required
def vendor_transactions(request):
    transactions_list = Transaction.objects.select_related('consumer__userprofileinfo').filter(vendor_id=request.user.id)
    transactions = get_pagenatied_items(request, transactions_list)

    context = {'transactions': transactions['data'], 'count': transactions['count']}
    return render(request, 'main_site/vendor_transactions.html', context)


@login_required
def consumer_dashboard(request):
    transaction_list = Transaction.objects.filter(consumer_id=request.user.id)
    transactions = get_pagenatied_items(request, transaction_list)

    context = {'transactions': transactions['data'], 'count': transactions['count']}
    return render(request, 'main_site/consumer_dashboard.html', context)


@login_required
def vendors(request):
    vendor_users_list = CustomUser.objects.filter(user_type='vendor')
    vendor_users = get_pagenatied_items(request, vendor_users_list)

    context = {'vendor_users': vendor_users['data'], 'count': vendor_users['count']}
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

            return redirect('main_site:consumer_purchase')

    context = {'vendor_user': vendor_user, 'transaction_form': transaction_form}
    return render(request, 'main_site/vendor.html', context)


def vendor_accept(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.vendor_status = 'Accepted'
    transaction.accepted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    transaction.save()

    return redirect('main_site:vendor_transactions')


def get_pagenatied_items(request, item_list):
    page = request.GET.get('page', 1)

    paginator = Paginator(item_list, 10)
    count = paginator.count
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    result = {'data': items, 'count': count}
    return result
