# Generated by Django 4.0.1 on 2022-03-30 10:42

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0008_remove_offer_title_offer_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price_net_unit', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('price_net', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('price_gross', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('vat', models.SmallIntegerField(choices=[(0, '0%'), (1, '8%'), (2, '23%')], default=2)),
                ('vat_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.offer')),
            ],
        ),
        migrations.DeleteModel(
            name='OfferItems',
        ),
    ]
