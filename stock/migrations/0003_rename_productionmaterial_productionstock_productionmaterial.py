# Generated by Django 4.0.1 on 2022-02-12 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_productionstock_production_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productionstock',
            old_name='ProductionMaterial',
            new_name='productionMaterial',
        ),
    ]
