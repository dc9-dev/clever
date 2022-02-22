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


class Production(models.Model):
    PREPARATION = 0
    DONE = 1
    STATUS = (
        (PREPARATION, 'w trakcie'),
        (DONE, 'zakończone'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS, default=PREPARATION)

    def __str__(self):
        return self.order


class ProductionMaterial(models.Model):

    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area =  models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)

    def _str__(self):

        return self.material
    

    def sum_area(self):

        return self.quantity * float(self.material.material_area)

    def stock_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        stock_area = 0

        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            stock_area += result

        return stock_area

    def stockIn_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        self.stockIn_area = 0

        for stock in material.productionstockin_set.all():
            result = stock.length * stock.width / 1000000
            self.stockIn_area += result

        return self.stockIn_area

    def total_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        total_area = 0
        
        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            total_area += result
        return total_area + self.quantity * float(self.material.material_area)

    def waste(self):

        material = ProductionMaterial.objects.get(id=self.id)

        total_area = 0 + self.quantity * float(self.material.material_area)
        
        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            total_area += result

        if float(self.area) - total_area + self.stockIn_area > 0:
            return 0
        else: 
            return abs(float(self.area) - total_area + self.stockIn_area)


class ProductionStock(models.Model):

    number = models.IntegerField(null=True)
    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE, related_name="stocks")
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.length, self.width)

class ProductionStockIn(models.Model):

    number = models.IntegerField(null=True)
    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE)
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.length, self.width)

class ProductionComments(models.Model):

    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=True, null=True)


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
    address = AddressField(on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GoodsReceivedNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, blank=False)
    material = models.ManyToManyField(Material, blank=False)
    documentID = models.CharField(max_length=255, blank=False, null=False)
    quantity = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} | {} - {}".format(self.material, self.documentID, self.contractor)

class GRNMaterial(models.Model):

    grn = models.ForeignKey(GoodsReceivedNote, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area =  models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)