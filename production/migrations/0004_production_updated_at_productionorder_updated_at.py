# Generated by Django 4.0.1 on 2023-01-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_productionorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productionorder',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
