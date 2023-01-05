# Generated by Django 3.2.3 on 2022-12-29 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryApp', '0030_merge_20221229_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesisdb',
            name='author',
        ),
        migrations.AlterField(
            model_name='authors',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thesis', to='libraryApp.thesisdb'),
        ),
    ]