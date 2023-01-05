# Generated by Django 4.0.1 on 2022-12-22 01:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0018_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='middle_initial',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator('[A-zA-z]+.', 'Invalid Middle Initial Format')]),
        ),
    ]