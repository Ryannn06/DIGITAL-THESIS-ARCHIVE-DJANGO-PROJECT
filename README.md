# Thesis Archive Management System
A Digital Thesis Archive for the Technological University of The Philippines- Cavite built in Django Framework.


## Table of Contents
- [General Information](#general-information)
- [Technologies](#technologies)
- [Installation and Setup](#installation-and-setup)
- [Key Features](#key-features)


## General Information
It is a capstone project develops a web-based application for the management of electronic thesis documents of Technological University of the Philippines- Cavite. This system allows the uploading, updating, and displaying of electronic thesis doucments given granted access.The front-end of this application is developed with HTML, CSS and Bootstrap. Meanwhile, back-end utilizes Python, Django, XAMPP, MySQL and Apache server. 


## Technologies
Below are the notable dependencies used in this project:
- django-crispy-forms=3.7.2
- django-allauth-0.60.0
- django-cleanup==6.0.0
- django-email-verification==0.2.2
- django-hitcount==1.3.5
- django-livereload-server==0.4
- django-taggit==2.1.0
- django-taggit-autosuggest==0.3.8
- django-tags-input==5.1.0
- django-utils-six==2.0
- numpy==1.23.3
- opencv-python==4.6.0.66
- pandas==1.5.0
- Pillow==9.2.0
- whitenoise==6.2.0
- django-ckeditor

## Installation and Setup
### 1. Run Development Server
1. Launh XAMPP; start Apache and MySQL Server.
2. On the command prompt, run:
> py manage.py runserver
3. Visit http://127.0.0.1:3000

### 2. Install Required Libraries
To install a [dependency](#technologies), run:
> pip install package-name

### 3. Make Migrations
This will create all the tables needed to operate the back-end of the application:
To make migrations, run:
> py manage.py makemigrations

### 4. After a successful migration, run:
> py manage.py migrate

## Key Features
- Requires account registration with email verification to ensure the security of the electronic thesis documents. The user can only use the organizational email address which he will then be asked to verify.
- Tracks the number of views for every thesis as theyare being viewed based on viewer's IP address and active time.
- The system develops its own auto-generated citations:APA, MLA, and Chicago for every thesis uploaded in the system.
- The user can dynamically populate the author field to allow the addition of multiple authors to a single thesis.


