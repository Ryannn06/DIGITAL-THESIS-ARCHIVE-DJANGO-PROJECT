# Generated by Django 4.0.1 on 2022-12-31 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0034_thesisdb_chicago'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestpdf',
            old_name='date_approve',
            new_name='date_evaluated',
        ),
    ]
