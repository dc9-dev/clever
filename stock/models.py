from django.db import models
from order.models import Material


class Warehouse(models.Model):
	name = models.CharField(max_length=255, default="magazyn")
	size = models.IntegerField(default=100)

	def __str__(self):
		return self.name

class Stock(models.Model):

    stock_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    length = models.DecimalField(max_digits=4, decimal_places=0)
    width = models.DecimalField(max_digits=4, decimal_places=0)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)


    def __str__(self):
    	return "#{} {}x{} {}".format(self.stock_id, self.length, self.width, self.material)

    def area(self):
        area = self.material
        return area