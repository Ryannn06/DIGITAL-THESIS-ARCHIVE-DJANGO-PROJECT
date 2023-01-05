from django.shortcuts import render, redirect
from .forms import RegisterForm, RegisterStaffForm
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
# Create your views here
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from libraryApp.tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage, BadHeaderError, send_mail, EmailMultiAlternatives
from django import template

from django.contrib.auth import authenticate, login
from django.db.models import Q

from django.core.exceptions import PermissionDenied


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    else:
        if request.method == 'POST':
            form =RegisterForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.is_student = True
                
                user.save()
                current_site = get_current_site(request)

                plaintext = template.loader.get_template('acc_active_emails/acc_active_email.txt')
                htmltemp = template.loader.get_template('acc_active_emails/acc_active_email.html')

                mail_subject = 'Activate your repository account.'
                message = {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': 'http',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                }
                
                text_content = plaintext.render(message)
                html_content = htmltemp.render(message)
                
                to_email = form.cleaned_data.get('email')

                email = EmailMultiAlternatives(
                            mail_subject, text_content,"Thesis Archive <do_not_reply@domain.example>", to=[to_email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return render(request, 'account_activation.html')
        else:
            form = RegisterForm()

        account = get_user_model()
        admin_account = account.objects.filter(is_staff=True, is_superuser=False, is_admin=True)

        context = {'form':form, 'admin_account':admin_account}
        return render(request, 'register/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        account = get_user_model()
        user = account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        messages.success(request,'Email Address has been verified successfully')
        return redirect('/accounts/login')
    else:
        messages.error(request,'Account Activition link invalid')
        return redirect('/')


def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    else:
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                account = get_user_model()
                associated_users = account.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        mail_subject = "Password Reset Requested"

                        plaintext = template.loader.get_template('password/password_reset_email.txt')
                        htmltemp = template.loader.get_template('password/password_reset_email.html')

                        c = {
                        "email":user.email,
                        'domain': 'technorepository.pythonanywhere.com',
                        'site_name': 'Thesis Archive',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        
                        #email = render_to_string(email_template_name, c)
                        text_content = plaintext.render(c)
                        html_content = htmltemp.render(c)

                        try:
                            email = EmailMultiAlternatives(
                                        mail_subject, text_content,"Thesis Archive <do_not_reply@domain.example>", to=[user.email]
                            )
                            email.attach_alternative(html_content, "text/html")
                            email.send()
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return render (request, "password/password_reset_done.html")

        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


def registerStaff(request):
    if request.user.is_authenticated:
        return redirect('/')

    else:
        account = get_user_model()
        admin_account = account.objects.filter(is_staff=True, is_superuser=False, is_admin=True)

        if admin_account.exists():
            raise PermissionDenied()

        else:
            if request.method == 'POST':
                form =RegisterStaffForm(request.POST)

                if form.is_valid():
                    form.save()

                    messages.success(request, 'Admin Account has been successfully registered! Login now.')
                    return redirect('/accounts/login')
            else:
                form = RegisterStaffForm()

            title = 'Admin'
            context = {'form':form, 'title':title}
            return render(request, 'register/register.html', context)
