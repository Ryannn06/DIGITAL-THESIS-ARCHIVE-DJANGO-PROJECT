# Generated by Django 3.2.3 on 2022-12-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0003_thesisdb_image_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestpdf',
            name='request_status',
            field=models.CharField(choices=[('Approve', 'Approve')], default='Pending', max_length=10),
        ),
    ]
