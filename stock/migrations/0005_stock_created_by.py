# Generated by Django 4.0.1 on 2022-08-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_comment_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='created_by',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
