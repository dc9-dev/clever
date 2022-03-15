from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('account/', include('account.urls')),
    path('stock/', include('stock.urls')),
    path('production/', include('production.urls')),
    path('pdf/', include('pdf.urls')),
] 