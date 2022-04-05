from django.conf import settings
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField
from decimal import Decimal


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Warehouse(models.Model):
    title = models.CharField(max_length=255)


class Material(models.Model):

    short_name = models.CharField(max_length=255, blank=False, null=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    quantity = models.SmallIntegerField(default=0, blank=False, null=True)
    material_area = models.DecimalField(default=Decimal('5.796'), decimal_places=4, blank=False, max_digits=10)

    class Meta:
        verbose_name = "materiał"
        verbose_name_plural = "materiały"

    def __str__(self):
        return self.short_name

    def caluclate_material(self):

        return self.quantity * self.material_area


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    length = IntegerRangeField(min_value=50, max_value=2800, null=True)
    width = IntegerRangeField(min_value=50, max_value=2070, null=True)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE, related_name="stocks")

    def __str__(self):
        return "#{} {}x{} {}".format(self.id, self.length, self.width, self.material)


class Contractor(models.Model):
    name = models.CharField(max_length=200)
    nip = models.CharField(max_length=13)
    regon = models.CharField(max_length=13, blank=True)
    phone = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)
    #address = AddressField(on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Kontrahent"
        verbose_name_plural = "Kontrahenci"

    def __str__(self):
        return self.name


class GoodsReceivedNote(models.Model):
    TOCHECK = 0
    CHECKED = 1
    STATUS = (
        (TOCHECK, 'Niezatwierdzone'),
        (CHECKED, 'Zatwierdzone')
    )
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, blank=False)
    documentID = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS, default=TOCHECK)
    
    def save(self, *args, **kwargs):
        dt = timezone.now()
        counter = GoodsReceivedNote.objects.filter(date__month=dt.month).count()
        if self.pk is None:
            self.title = "PZ/{0:0=3d}/{1}".format(counter, dt.strftime("%m/%y"))
        super(GoodsReceivedNote, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.documentID, self.contractor)

    def total_net(self):
        materials = GoodsReceivedNote.objects.get(id=self.id).grnmaterial_set.all()
        
        total = 0
        for material in materials:
            total += material.price_net
        return total
    
    def total_vat(self):
        materials = GoodsReceivedNote.objects.get(id=self.id).grnmaterial_set.all()
        
        total = 0
        for material in materials:
            total += material.vat_amount
        return total
    
    def total_gross(self):
        materials = GoodsReceivedNote.objects.get(id=self.id).grnmaterial_set.all()
        
        total = 0
        for material in materials:
            total += material.price_gross
        return total


class GRNMaterial(models.Model):

    VAT_8 = 0
    VAT_23 = 1
    VAT = (
        (VAT_8, '8%'),
        (VAT_23, '23%')
    )
    
    grn = models.ForeignKey(GoodsReceivedNote, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    area = models.DecimalField(default=Decimal('0.000'), decimal_places=4, blank=False, max_digits=10)
    quantity = models.IntegerField(blank=True, null=True)
    price_net_unit = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    price_net = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    price_gross = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)
    vat = models.SmallIntegerField(choices=VAT, default=VAT_23)
    vat_amount = models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=False, max_digits=10)

    def save(self, *args, **kwargs):
        self.price_net = float(self.price_net_unit) * float(self.area)
        self.quantity = self.area / self.material.material_area
        self.price_gross = self.price_gross_calc()
        self.vat_amount = self.vat_amount_calc()
        super(GRNMaterial, self).save(*args, **kwargs)
    
    def vat_amount_calc(self):
        
        return float(self.price_gross) - self.price_net

    def price_gross_calc(self):
        vat = 0
        if self.vat == self.VAT_8:
            vat = 0.08
        if self.vat == self.VAT_23:
            vat = 0.23
        return float(self.price_net) + (float(self.price_net) * float(vat))

