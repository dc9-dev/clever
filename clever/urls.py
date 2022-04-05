from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', include('production.urls')),
    path('account/', include('account.urls')),
    path('', include('stock.urls')),
    path('production/', include('production.urls')),
    path('pdf/', include('pdf.urls')),
    path('cash/', include('cash.urls')),
    path('offer/', include('offer.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
