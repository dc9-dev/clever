from django.conf import settings
from django.db import models
from django.urls import reverse

from randomslugfield import RandomSlugField


class Order(models.Model):
    PENDING = 0
    DURING = 1
    DONE = 2
    STATUS = (
        (PENDING, 'Oczekuję'),
        (DURING, 'W trakcie'),
        (DONE, 'Zakończone'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slug = RandomSlugField(length=7, exclude_lower=True, exclude_upper=True, exclude_vowels=True)
    status = models.SmallIntegerField(choices=STATUS, default=PENDING)

    class Meta:
        verbose_name = "zamówienie"
        verbose_name_plural = "zamówienia"

    def __str__(self):
        return "Zamówienie ID#{} z dnia {}".format(self.slug, self.date_created.strftime('%d/%m/%y'))

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})


class Pattern(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "wzór"
        verbose_name_plural = "wzory"

    def __str__(self):
        return self.name

class Milling(models.Model):
    
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = "frez"
        verbose_name_plural = "frezy"

    def __str__(self):
        return self.name
     

class Item(models.Model):

    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    lenght = models.DecimalField(max_digits=4, decimal_places=0)
    width = models.DecimalField(max_digits=4, decimal_places=0)
    lenght = models.PositiveSmallIntegerField(blank=False)
    quantity = models.SmallIntegerField(default=1, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    lenght1 = models.BooleanField(default=False)
    lenght2 = models.BooleanField(default=False)
    width1 = models.BooleanField(default=False)
    width2 = models.BooleanField(default=False)

    class Meta:

        verbose_name = "formatka"
        verbose_name_plural = "formatki"

    def __str__(self):
        return "{} x {}".format(self.width, self.lenght)
