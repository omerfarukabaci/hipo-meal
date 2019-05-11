# Generated by Django 2.2.1 on 2019-05-11 18:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_evalutation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evalutation',
            name='recipe_vote',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
