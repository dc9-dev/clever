# Generated by Django 4.0.1 on 2022-03-20 18:15

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionmaterial',
            name='waste_field',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.000'), max_digits=10),
        ),
    ]
