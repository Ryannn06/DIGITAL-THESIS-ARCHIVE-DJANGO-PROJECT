# Generated by Django 4.0.1 on 2022-12-22 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0021_rename_apa_thesisdb_apa_citation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisdb',
            name='author',
        ),
    ]