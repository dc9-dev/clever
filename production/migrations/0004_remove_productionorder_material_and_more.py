# Generated by Django 4.0.1 on 2022-03-01 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('production', '0003_alter_productionorder_material_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productionorder',
            name='material',
        ),
        migrations.AddField(
            model_name='productionorder',
            name='material',
            field=models.ManyToManyField(blank=True, null=True, to='order.Material'),
        ),
        migrations.RemoveField(
            model_name='productionorder',
            name='services',
        ),
        migrations.AddField(
            model_name='productionorder',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='production.Services'),
        ),
    ]
