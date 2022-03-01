from django.conf import settings
from django.db import models
from order.models import Material, IntegerRangeField
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField

from decimal import Decimal


class Stock(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800, null=True)
    width = IntegerRangeField(min_value=50, max_value=2070, null=True)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")

    def __str__(self):
    	return "#{} {}x{} {}".format(self.id, self.length, self.width, self.material)


class Cutter(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=False, null=True)
    toBuy = models.IntegerField(blank=True, null=True, default=0)
    forSharpening = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class Contractor(models.Model):
    name = models.CharField(max_length=200)
    nip = models.CharField(max_length=13)
    regon = models.CharField(max_length=13, blank=True)
    phone = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)
    #address = AddressField(on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GoodsReceivedNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, blank=False)
    documentID = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.documentID, self.contractor)


class GRNMaterial(models.Model):

    grn = models.ForeignKey(GoodsReceivedNote, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area = models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):

        self.quantity = self.area / self.material.material_area
        super(GRNMaterial, self).save(*args, **kwargs)

