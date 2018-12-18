from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import UserForm, UserProfileInfoForm, UserPaymentInfoForm


def logout_view(request):
    """Log the user out."""
    logout(request)
    return redirect('main_site:index')


def register_consumer_view(request):
    return redirect('main_site:index')


def register_vendor_view(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        payment_form = UserPaymentInfoForm()
    else:
        # Process completed form.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        payment_form = UserPaymentInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and payment_form.is_valid():
            new_user = user_form.save()
            new_user.email = new_user.username
            new_user.set_password(new_user.password)
            new_user.user_type = 'vendor'
            profile = profile_form.save(commit=False)
            profile.user = new_user
            payment = payment_form.save(commit=False)
            payment.user = new_user
            payment.pay_amount = 20

            new_user.save()
            profile.save()
            payment.save()
            # Log the user in, and then redirect to home page.
            # authenticated_user = authenticate(username=new_user.username,
            #                                   password=request.POST['password1'])
            # login(request, authenticated_user)
            return redirect('main_site:index')

    context = {'user_form': user_form, 'profile_form': profile_form, 'payment_form': payment_form}
    return render(request, 'users/register_vendor.html', context)
