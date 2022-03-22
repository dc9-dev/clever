from django.conf import settings
from django.db import models
from decimal import Decimal


class Cash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    
    class Meta:
        verbose_name = "Kasa"
        verbose_name_plural = "Kasy"

    def __str__(self):
        return "{} - {} {}".format(self.title, self.user.first_name, self.user.last_name)


class Payment(models.Model):
    UNCHECKED = 0
    CHECKED = 1

    CHOICES = (
        (UNCHECKED, 'Niesprawdzony'),
        (CHECKED, 'Sprawdzony')
    )

    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True)
    IW_IY = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    cash_amount = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10, editable=False)
    status = models.PositiveSmallIntegerField(choices=CHOICES, default=UNCHECKED)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if self.status == 0:
            cash = Cash.objects.get(id=self.cash.id)
            cash.amount += self.amount
            self.cash_amount = cash.amount
            cash.save()
        super(Payment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cash = Cash.objects.get(id=self.cash.id)
        cash.amount -= self.amount
        cash.save()
        super(Payment, self).delete(*args, **kwargs)