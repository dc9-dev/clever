from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import F, Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import make_aware
from order.models import Material, IntegerRangeField

from decimal import Decimal
from datetime import datetime



class Production(models.Model):
    PREPARATION = 0
    PENDING = 1
    DURING = 2
    DONE = 3
    STATUS = (
        ('zmień status', 'zmień status'),
        (PREPARATION, 'Przygotowywanie'),
        (PENDING, 'Oczekuję'),
        (DURING, 'W trakcie'),
        (DONE, 'Zakończone'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS, default=DURING)

    def __str__(self):
        return self.order

    def save(self, *args, **kwargs):
        rename = list(self.order)
        rename[0] = 'P'
        rename[1] = 'R'
        self.order = ''.join(rename)
        super(Production, self).save(*args, **kwargs)


class ProductionMaterial(models.Model):

    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area = models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)

    def _str__(self):

        return self.material

    def sum_area(self):

        return self.quantity * float(self.material.material_area)

    def stock_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        stock_area = 0

        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            stock_area += result

        return stock_area

    def stockIn_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        self.stockIn_area = 0

        for stock in material.productionstockin_set.all():
            result = stock.length * stock.width / 1000000
            self.stockIn_area += result

        return self.stockIn_area

    def total_area(self):

        material = ProductionMaterial.objects.get(id=self.id)

        total_area = 0

        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            total_area += result
        return total_area + self.quantity * float(self.material.material_area)

    def waste(self):

        material = ProductionMaterial.objects.get(id=self.id)

        total_area = 0 + self.quantity * float(self.material.material_area)

        for stock in material.stocks.all():
            result = stock.length * stock.width / 1000000
            total_area += result

        if float(self.area) - total_area + self.stockIn_area > 0:
            return 0
        else:
            return abs(float(self.area) - total_area + self.stockIn_area)

    def waste_precent(self):

        if self.waste != 0 and self.total_area != 0 and self.quantity != 0:
            return  (self.waste() / self.total_area() ) * 100
            
        else:
            return 0
            
        


class ProductionStock(models.Model):

    number = models.IntegerField(null=True)
    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE, related_name="stocks")
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.length, self.width)


class ProductionStockIn(models.Model):

    number = models.IntegerField(null=True)
    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE)
    length = IntegerRangeField(min_value=50, max_value=2800)
    width = IntegerRangeField(min_value=50, max_value=2070)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.length, self.width)


class ProductionComments(models.Model):

    productionMaterial = models.ForeignKey(ProductionMaterial, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=True, null=True)


class Customer(models.Model):

    email = models.EmailField(unique=True, blank=True)
    company = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    # Delivery details
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

    def __str__(self):
        return self.company


class Services(models.Model):

    title = models.CharField(max_length=255)
    # price_gross = models.IntegerField()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "usługa"
        verbose_name_plural = "usługi"


class ProductionOrder(models.Model):
    PREPARATION = 0
    PENDING = 1
    DURING = 2
    DONE = 3
    STATUS = (
        (PREPARATION, 'Przygotowywanie'),
        (PENDING, 'Oczekuję'),
        (DURING, 'W trakcie'),
        (DONE, 'Zakończone'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS, default=PREPARATION)

    def save(self, *args, **kwargs):
        dt = timezone.now()
        if self.pk is not None:
            orig = ProductionOrder.objects.get(id=self.id)
            if orig.status != self.status:
                self.mail()
        else:
            counter = ProductionOrder.objects.filter(date__month=dt.month).count()
            self.order = "ZO/{0:0=3d}/{1}".format(counter, dt.strftime("%m/%y"))
        super(ProductionOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.order

    def get_total(self):
        total = 0 
        for i in self.materialservices_set.all():
            result = i.price * i.area
            total += result
        return total

    def mail(self, *args, **kwargs):

        ctx = {
            'name': self.customer,
            'status': self.get_status_display,
        }

        template = render_to_string('production/email_template.html', ctx)
        subject, from_email, to = 'Zamówienie nr {} - status: {}'.format(self.order, self.get_status_display()), settings.EMAIL_HOST_USER, self.customer.email
        text_content = 'Test test test.'
        html_content = render_to_string('production/email_template.html', ctx)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class MaterialServices(models.Model):

    productionorder = models.ForeignKey(ProductionOrder,
                                        on_delete=models.CASCADE)
    material = models.ForeignKey(Material,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    services = models.ForeignKey(Services,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    area = models.DecimalField(default=Decimal('0.000'), decimal_places=3, blank=False, max_digits=10)
    price = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    #transport = models.BooleanField(default=0)

    def total(self):
        return self.area * self.price
