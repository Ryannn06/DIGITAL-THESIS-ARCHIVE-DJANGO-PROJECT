# Generated by Django 4.0.1 on 2022-12-18 06:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0009_alter_requestpdf_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesisdb',
            name='author',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator('^[A-Z]\\w+,\\s*[A-Z]\\.(?:\\s+and (?:[A-Z]\\w+,\\s*[A-Z]\\.|et\\.\\s+al\\.))?', 'Invalid Format')]),
        ),
        migrations.AlterField(
            model_name='thesisdb',
            name='published_status',
            field=models.CharField(choices=[('Approved', 'Approve'), ('Rejected', 'Reject')], default='Pending', max_length=10),
        ),
    ]