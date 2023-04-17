# Generated by Django 4.0.1 on 2023-04-13 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_remove_material_material_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='gender',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='stock.gender'),
        ),
    ]
