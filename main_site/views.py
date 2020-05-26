from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import CustomUser, UserProfileInfo
from .models import Transaction
from .forms import PhoneVerificationForm, TransactionForm, EmailSearchForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def index(request):
    """The home page for Newark Shop."""
    user = request.user
    if user.is_authenticated:
        user_type = request.user.user_type
        if user.is_superuser:
            return redirect('main_site:admin_dashboard')
        else:
            if user_type == 'vendor':
                return redirect('main_site:vendor_dashboard')
            if user_type == 'consumer':
                return redirect('main_site:consumer_dashboard')

    return render(request, 'main_site/index.html')


@login_required
def admin_dashboard(request):
    transactions_list = Transaction.objects.all()
    total_sales = 0
    for transaction in transactions_list:
        transaction.amount = set_digit_format(transaction.amount)
        total_sales += float(transaction.amount)

    total_sales = set_digit_format(total_sales)
    transaction_count = Transaction.objects.all().count()

    transactions = get_pagenatied_items(request, transactions_list)

    # for transaction in transactions:
    #     transaction.current_index = transactions.start_index() + transactions.index(transaction)

    # for i, item in enumerate(transactions):
    #     print(i == transactions.index(item))
    #     print(i)
    #     print(item)
    transactions = add_property(transactions)

    context = {
        'transactions': transactions,
        'transaction_count': transaction_count,
        'total_sales': total_sales,
    }
    return render(request, 'main_site/admin_dashboard.html', context)


@login_required
def admin_transactions(request):
    consumer_list = CustomUser.objects.raw(
        '''SELECT t.id, u.username, SUM(t.amount) total_amount
            FROM main_site_transaction as t
            RIGHT JOIN users_customuser as u ON t.consumer_id = u.id
            WHERE u.user_type = 'consumer'
            GROUP BY u.username
            ORDER BY total_amount DESC''')

    for consumer in consumer_list:
        if consumer.total_amount is None:
            consumer.total_amount = 0
        consumer.total_amount = set_digit_format(consumer.total_amount)

    consumer_count = CustomUser.objects.filter(user_type='consumer').count()
    consumers = get_pagenatied_items(request, consumer_list)
    consumers = add_property(consumers)
    context = {
        'consumers': consumers,
        'consumer_count': consumer_count
    }

    return render(request, 'main_site/admin_transactions.html', context)


@login_required
def admin_users(request):
    users_list = CustomUser.objects.filter(is_superuser=0)
    count = users_list.count()
    users = get_pagenatied_items(request, users_list)
    users = add_property(users)

    context = {
        'users': users,
        'count': count,
    }
    return render(request, 'main_site/admin_users.html', context)


@login_required
def admin_user_delete(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()

    return redirect('main_site:admin_users')


@login_required
def vendor_dashboard(request):
    transactions_list = Transaction.objects.filter(vendor_id=request.user.id)
    total_count = transactions_list.count()
    total_sales = 0
    for transaction in transactions_list:
        transaction.amount = set_digit_format(transaction.amount)
        total_sales += float(transaction.amount)

    total_sales = set_digit_format(total_sales)
    transactions = get_pagenatied_items(request, transactions_list)

    context = {
        'transactions': transactions,
        'total_count': total_count,
        'total_sales': total_sales,
        'vendor_name': request.user.userprofileinfo.business_name
    }
    return render(request, 'main_site/vendor_dashboard.html', context)


@login_required
def vendor_transactions(request):
    # transactions_list = Transaction.objects.select_related('consumer__userprofileinfo').filter(vendor_id=request.user.id)
    # transactions = get_pagenatied_items(request, transactions_list)
    #
    # context = {'transactions': transactions['data'], 'count': transactions['count']}
    # return render(request, 'main_site/vendor_transaction.html', context)
    return redirect('main_site:vendor_phone_verification')


@login_required
def vendor_phone_verification(request):
    if request.method != 'POST':
        phone_verification_form = PhoneVerificationForm()
    else:
        phone_verification_form = PhoneVerificationForm(data=request.POST)
        if phone_verification_form.is_valid():
            phone_number = phone_verification_form.data['phone_number']
            consumers = UserProfileInfo.objects.filter(phone_number=phone_number)
            # if not consumers.count():
            #     context = {'phone_verification_form': phone_verification_form, 'consumer_not_exist': True}
            #     return render(request, 'main_site/phone_verification.html', context)
            # else:
            #     consumer_id = consumers[0].user_id
            consumer_id = consumers[0].user_id
            return redirect('main_site:vendor_transaction', consumer_id)

    context = {'phone_verification_form': phone_verification_form}
    return render(request, 'main_site/phone_verification.html', context)


@login_required
def vendor_transaction(request, consumer_id):
    if request.method != 'POST':
        transaction_form = TransactionForm()
        consumer = CustomUser.objects.get(id=consumer_id)
    else:
        transaction_form = TransactionForm(data=request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.consumer_id = consumer_id
            transaction.vendor_id = request.user.id
            transaction.save()

            return redirect('main_site:vendor_dashboard')

    context = {
        'transaction_form': transaction_form,
        'consumer': consumer
    }
    return render(request, 'main_site/vendor_transaction.html', context)


@login_required
def consumer_dashboard(request):
    transactions_list = Transaction.objects.filter(consumer_id=request.user.id)
    # transaction_count = transaction_list.count()
    # transactions = get_pagenatied_items(request, transactions_list)
    total_count = transactions_list.count()
    total_sales = 0
    for transaction in transactions_list:
        transaction.amount = set_digit_format(transaction.amount)
        total_sales += float(transaction.amount)

    total_sales = set_digit_format(total_sales)
    transactions = get_pagenatied_items(request, transactions_list)

    context = {
        'transactions': transactions,
        'total_count': total_count,
        'toatal_sales': total_sales
    }
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


def get_pagenatied_items(request, item_list, per_page=10):
    page = request.GET.get('page', 1)

    paginator = Paginator(item_list, per_page)
    count = paginator.count
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # result = {'data': items, 'count': count}
    return items


def add_property(list_object):
    for item_object in list_object:
        item_object.current_index = list_object.start_index() + list_object.index(item_object)

    return list_object


def set_digit_format(_value):
    value = float(_value)
    value = "{0:.2f}".format(value)
    return value
