# Generated by Django 4.0.1 on 2023-01-13 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0012_registrations_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrations',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='requestpdf',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='thesisdb',
            name='is_read',
        ),
    ]
