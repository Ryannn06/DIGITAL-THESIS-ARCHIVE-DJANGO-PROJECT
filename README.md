# Thesis Archive Management System
A Digital Thesis Archive for Technological University of The Philippines- Cavite created in Django Framework.

## Install Required Libraries
This will handle the design for our form inputs
> pip install django-crispy-forms
This will handle for the django authenticaton
> pip install django-allauth
This plugin automatically removes the file from the local folder when deleted from the database.
> django-cleanup==6.0.0

django-email-verification==0.2.2

django-hitcount==1.3.5

django-livereload-server==0.4
django-taggit==2.1.0
django-taggit-autosuggest==0.3.8
django-tags-input==5.1.0
django-tinymce==3.4.0
django-utils-six==2.0
Django-Verify-Email==2.0.3
django-widget-tweaks==1.4.12
gunicorn==20.1.0
lazy-object-proxy==1.4.3
matplotlib==3.3.3
numpy==1.23.3
oauthlib==3.2.0
opencv-python==4.6.0.66
pandas==1.5.0
Pillow==9.2.0
psycopg2==2.9.5
reportlab==3.6.10
requests==2.27.1
requests-oauthlib==1.3.1
virtualenv==20.1.0
whitenoise==6.2.0

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


