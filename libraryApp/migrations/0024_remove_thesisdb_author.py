# Generated by Django 4.0.1 on 2022-12-23 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0023_thesisdb_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisdb',
            name='author',
        ),
    ]
