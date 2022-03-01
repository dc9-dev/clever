from django.contrib import admin
from .models import MaterialServices, Customer, Services

# Register your models here.

admin.site.register(Customer)
admin.site.register(Services)
admin.site.register(MaterialServices)
