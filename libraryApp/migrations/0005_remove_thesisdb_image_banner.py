# Generated by Django 4.0.1 on 2022-12-18 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0004_rename_department_head_coldept_department_abbreviation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisdb',
            name='image_banner',
        ),
    ]
