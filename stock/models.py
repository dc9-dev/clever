from django.conf import settings
from django.db import models
from order.models import Material, IntegerRangeField



class Stock(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800, null=True)
    width = IntegerRangeField(min_value=50, max_value=2070, null=True)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")

    def __str__(self):
    	return "#{} {}x{} {}".format(self.id, self.length, self.width, self.material)


class ProductionStock(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.CharField(max_length=200)

    def __str__(self):
        return "{} x {} {}".format(self.length, self.width, self.material)

class Production(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, blank=True)
    materialUsed = models.IntegerField(default=0)
    productionStocks = models.ManyToManyField(ProductionStock, blank=True)

    def __str__(self):
        return "{} | {} {}".format(self.order, self.user.first_name, self.user.last_name)
