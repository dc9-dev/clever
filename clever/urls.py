from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('account/', include('account.urls')),
    path('stock/', include('stock.urls')),
    path('production/', include('production.urls')),
    path('pdf/', include('pdf.urls')),
    path('cash/', include('cash.urls')),
    path('offer/', include('offer.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
