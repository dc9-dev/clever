from django.conf import settings
from django.db import models
from order.models import Material, IntegerRangeField

from decimal import Decimal


class Stock(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800, null=True)
    width = IntegerRangeField(min_value=50, max_value=2070, null=True)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")

    def __str__(self):
    	return "#{} {}x{} {}".format(self.id, self.length, self.width, self.material)


class Production(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} | {} {}".format(self.order, self.user.first_name, self.user.last_name)


class ProductionMaterial(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area =  models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.SmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.material

    def total_area(self):
        
        return self.quantity * self.material.material_area


class ProductionStock(models.Model):
    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE, related_name="stocks")
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {} {}".format(self.length, self.width, self.productionMaterial)

    def total_area(self):

        total_area = 0
        for stock in ProductionStock.objects.filter(material=self.material):
            result = stock.length * stock.width / 1000000
            total_area += result


class Cutter(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=False, null=True)
    toBuy = models.IntegerField(blank=True, null=True, default=0)
    forSharpening = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name

