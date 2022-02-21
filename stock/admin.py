from django.contrib import admin
from .models import *

admin.site.register(Stock),
admin.site.register(Production),
admin.site.register(Cutter),
admin.site.register(Contractor),
admin.site.register(GoodsReceivedNote),