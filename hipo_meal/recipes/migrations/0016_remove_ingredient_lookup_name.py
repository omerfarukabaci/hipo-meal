# Generated by Django 2.2.1 on 2019-05-13 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_ingredient_lookup_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='lookup_name',
        ),
    ]
