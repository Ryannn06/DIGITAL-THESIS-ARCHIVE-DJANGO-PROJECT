# Generated by Django 4.0.1 on 2022-12-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0032_thesisdb_apa'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesisdb',
            name='mla',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]