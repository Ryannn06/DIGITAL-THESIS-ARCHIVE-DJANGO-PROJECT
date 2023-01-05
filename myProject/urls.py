"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from register import views as v
from libraryApp import views
#from allauth.account import views as allauth_views

urlpatterns = [
    path('', include('libraryApp.urls')),
    path('admin/', admin.site.urls),
    path('register/', v.register, name='register'),
    path('register_admin/', v.registerStaff, name='registerStaff'),
    path('accounts/login/', views.auth_login, name='login'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('accounts/password_change/', views.password_change, name='password_change'),

    path('accounts/', include('django.contrib.auth.urls')),


    #path('accounts/', include('allauth.urls')),
]

handler404 = 'libraryApp.views.page_not_found'