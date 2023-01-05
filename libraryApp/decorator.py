from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def for_students(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/'):
    '''
    A decorator to check logged in user could be a student and redirects to the login page if the user isn't authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def for_admin(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/'):
    '''
    A decorator to check logged in user could be an admin and redirects to the login page if the user isn't authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
