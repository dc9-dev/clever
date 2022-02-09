from django.contrib import admin
from .models import *

admin.site.register(Stock),
admin.site.register(Production),
admin.site.register(ProductionStock),
admin.site.register(Cutter),