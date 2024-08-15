# Generated by Django 5.1 on 2024-08-15 09:15

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query_api', '0005_alter_query_latitude_alter_query_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('-90')), django.core.validators.MaxValueValidator(Decimal('90'))]),
        ),
    ]
