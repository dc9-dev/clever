from django.db import models
from order.models import Material, IntegerRangeField


class Warehouse(models.Model):
	name = models.CharField(max_length=255, default="magazyn")
	size = models.IntegerField(default=100)

	def __str__(self):
		return self.name

class Stock(models.Model):

    stock_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)


    def __str__(self):
    	return "#{} {}x{} {}".format(self.stock_id, self.length, self.width, self.material)