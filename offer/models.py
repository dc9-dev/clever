
from django.conf import settings 
from django.db import models
from account.models import Customer
from decimal import Decimal
import datetime

class Offer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        counter = Offer.objects.count() + 1
        self.number = "{}/{}".format(counter, datetime.datetime.today().year)
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return "Oferta nr {} - {}".format(self.number, self.customer.company)

    def total_net(self):
        items = Offer.objects.get(id=self.id).offeritem_set.all()
        
        total = 0
        for item in items:
            total += item.price_net
        return total
    
    def total_vat(self):
        items = Offer.objects.get(id=self.id).offeritem_set.all()
        
        total = 0
        for item in items:
            total += item.vat_amount
        return total
    
    def total_gross(self):
        items = Offer.objects.get(id=self.id).offeritem_set.all()
        
        total = 0
        for item in items:
            total += item.price_gross
        return total


class OfferItem(models.Model):

    VAT_0 = 0
    VAT_8 = 1
    VAT_23 = 2
    VAT = (
        (VAT_0, '0%'),
        (VAT_8, '8%'),
        (VAT_23, '23%'),
    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField(blank=False, null=True)
    price_net_unit = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    price_net = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    price_gross = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    vat = models.SmallIntegerField(choices=VAT, default=VAT_23)
    vat_amount = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)

    def vat_amount_calc(self):
        
        return float(self.price_gross) - self.price_net

    def price_gross_calc(self):
        vat = 0
        if self.vat == self.VAT_0:
            vat = 0
        if self.vat == self.VAT_8:
            vat = 0.08
        if self.vat == self.VAT_23:
            vat = 0.23
        return float(self.price_net) + (float(self.price_net) * float(vat))
    
    def save(self, *args, **kwargs):
        self.price_net = float(self.price_net_unit) * float(self.quantity)
        self.price_gross = self.price_gross_calc()
        self.vat_amount = self.vat_amount_calc()
        super(OfferItem, self).save(*args, **kwargs)

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    content = models.TextField()
    visible = models.BooleanField(default=False)