from django.conf import settings
from django.db import models
from order.models import Material, IntegerRangeField


class Warehouse(models.Model):
	name = models.CharField(max_length=255, default="magazyn")
	size = models.IntegerField(default=100)

	def __str__(self):
		return self.name


class Stock(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
   
    def __str__(self):
    	return "#{} {}x{} {}".format(self.id, self.length, self.width, self.material)



class Production(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, blank=True)
    materialUsed = models.IntegerField(default=0)

    def __str__(self):
        return "{} | {} {}".format(self.order, self.user.first_name, self.user.last_name)

class Formatka(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    production = models.ForeignKey(Production, null=True, on_delete=models.CASCADE)

class Spad(models.Model):

    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    production = models.ForeignKey(Production, null=True, on_delete=models.CASCADE)
