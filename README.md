# Thesis Archive Management System
A Digital Thesis Archive for Technological University of The Philippines- Cavite created in Django Framework.

## Install Required Plugins
To install a library or plugin, run:
> pip install ( name of the plugin )
1. django-crispy-forms
2. django-allauth
3. django-cleanup==6.0.0
4. django-email-verification==0.2.2
5. django-hitcount==1.3.5
6. django-livereload-server==0.4
7. django-taggit==2.1.0
8. django-taggit-autosuggest==0.3.8
9. django-tags-input==5.1.0
10. django-utils-six==2.0
11. numpy==1.23.3
12. opencv-python==4.6.0.66
13. pandas==1.5.0
14. Pillow==9.2.0
15. whitenoise==6.2.0

## Run Devvelopment Server
1. Launh XAMPP; start Apache and MySQL Server.
2. On the command prompt, run:
> py manage.py runserver
3. Visit localhost:3000/

## Make Migrations
This will create all the tables needed to operate the back-end of the application:
To make migrations, run:
> py manage.py makemigrations

After a successful migration, run:
> py manage.py migrate


