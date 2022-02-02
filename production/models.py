from django.db import models
from django.conf import settings

from order.models import Material

class Production(models.Model):

    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    comments = models.TextField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now_add=True)