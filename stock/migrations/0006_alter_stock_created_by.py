# Generated by Django 4.0.1 on 2022-08-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_stock_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='created_by',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
