# Generated by Django 4.0.1 on 2023-01-13 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0011_registrations_is_read_requestpdf_is_read_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrations',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
