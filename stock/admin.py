from django.contrib import admin
from .models import Stock, Contractor, GoodsReceivedNote, Material, Gender

admin.site.register(Stock),
admin.site.register(Material),
admin.site.register(Contractor),
admin.site.register(GoodsReceivedNote),
admin.site.register(Gender),
#admin.site.register(GRNMaterial),