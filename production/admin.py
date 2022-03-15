from django.contrib import admin
from .models import Customer, Services, ProductionOrder

# Register your models here.

admin.site.register(Customer)
admin.site.register(Services)
admin.site.register(ProductionOrder)
