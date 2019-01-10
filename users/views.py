from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import UserForm, UserProfileInfoForm, UserPaymentInfoForm

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy
from django.conf import settings


def logout_view(request):
    """Log the user out."""
    logout(request)
    return redirect('main_site:index')


def register_consumer_view(request):
    if request.method != 'POST':
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    else:
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            new_user.email = new_user.username
            new_user.set_password(new_user.password)
            new_user.user_type = 'consumer'
            profile = profile_form.save(commit=False)
            profile.user = new_user

            new_user.save()
            profile.save()

            return redirect('main_site:index')

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'users/register_consumer.html', context)


def register_step_one(request):
    user_type = get_user_type(request)

    if request.method != 'POST':
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    else:
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            if user_type == 'consumer':
                return redirect('users:registerConsumerStepTwo')
            elif user_type == 'vendor':
                return redirect('users:registerVendorStepTwo')

    context = {'user_form': user_form, 'profile_form': profile_form, 'user_type': user_type}
    return render(request, 'users/register_step1.html', context)


def register_step_two(request):
    return render(request, 'users/register_step2.html')


def register_step_three(request):
    if request.method != 'POST':
        payment_form = UserPaymentInfoForm()
    else:
        payment_form = UserPaymentInfoForm(data=request.POST)
        if payment_form.is_valid():
            return redirect('users:registerVendorStepFour')

    context = {'payment_form': payment_form}
    return render(request, 'users/register_step3.html', context)


def register_step_four(request):
    user_type = get_user_type(request)
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

        if user_type == 'consumer':
            if user_form.is_valid() and profile_form.is_valid():
                new_user = user_form.save()
                new_user.email = new_user.username
                new_user.set_password(new_user.password)
                new_user.user_type = user_type
                profile = profile_form.save(commit=False)
                profile.user = new_user

                new_user.save()
                profile.save()

        elif user_type == 'vendor':
            if user_form.is_valid() and profile_form.is_valid() and payment_form.is_valid():
                new_user = user_form.save()
                new_user.email = new_user.username
                new_user.set_password(new_user.password)
                new_user.user_type = user_type
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
        else:
            pass

        return redirect('main_site:index')

    context = {'user_form': user_form, 'profile_form': profile_form,
               'payment_form': payment_form, 'user_type': user_type}
    return render(request, 'users/register_step4.html', context)


def get_user_type(request):
    path = request.path
    if path.find('vendor') > 0:
        user_type = 'vendor'
    elif path.find('consumer') > 0:
        user_type = 'consumer'
    else:
        user_type = 'admin'

    return user_type


# class ExtPasswordResetView(auth_views.PasswordResetView):
#     template_name = 'users/password_reset.html',
#     email_template_name = 'users/password_reset_email.html',
#     subject_template_name = 'users/password_reset_subject.txt',
#     from_email = settings.DEFAULT_FROM_EMAIL,
#     success_url = reverse_lazy('users:password_reset_done')
#
#
# password_reset_view = ExtPasswordResetView.as_view()
#
#
# class ExtPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     template_name = 'users/password_reset_confirm.html',
#     success_url = reverse_lazy('users:password_reset_complete')
#     # form_class = SetPasswordForm
#
#
# password_reset_confirm = ExtPasswordResetConfirmView.as_view()
