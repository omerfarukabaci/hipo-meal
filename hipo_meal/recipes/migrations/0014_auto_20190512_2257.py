# Generated by Django 2.2.1 on 2019-05-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20190512_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=75, unique=True),
        ),
    ]
