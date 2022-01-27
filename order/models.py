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
    title = models.CharField(max_length=255, blank=False, null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slug = RandomSlugField(length=7, exclude_lower=True, exclude_upper=True, exclude_vowels=True)
    attachment = models.FileField(upload_to ='zamowienie/')
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

class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return ''
        return int(value) # return 0/1

class Material(models.Model):

    short_name = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "materiał"
        verbose_name_plural = "materiały"

    def __str__(self):
        return self.short_name

class Stock(models.Model):

    stock_id = models.CharField(max_length=255, blank=True, null=True)
    length = models.DecimalField(max_digits=4, decimal_places=0)
    width = models.DecimalField(max_digits=4, decimal_places=0)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE)

class Item(models.Model):

    item_number = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    length = models.DecimalField(max_digits=4, decimal_places=0)
    width = models.DecimalField(max_digits=4, decimal_places=0)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    length1 = CustomBooleanField()
    length2 = CustomBooleanField()
    width1 = CustomBooleanField()
    width2 = CustomBooleanField()

    class Meta:

        verbose_name = "formatka"
        verbose_name_plural = "formatki"

    def __str__(self):
        return "{} x {}".format(self.width, self.length)
