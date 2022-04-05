from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from .forms import (AttachmentForm,
                    ProductionCommentsForm,
                    CreateOrderForm,
                    EditOrderForm,
                    CommentForm)
from .models import (MaterialServices, Production,
                     ProductionStock,
                     ProductionMaterial,
                     ProductionComments,
                     ProductionOrder,
                     )
from .filters import ProductionOrderFilter

from clever.decorators import staff_or_404
from stock.models import Stock
from stock.forms import StockCreateForm, StockCreateInForm
from stock.filters import StockFilter
from stock.models import Material


@staff_or_404
def ProductionHome(request):
    
    productions_pending = Production.objects.filter(status=1).order_by('-date')[:25]
    productions_during = Production.objects.filter(status=2).order_by('-date')[:25]
    productions_done = Production.objects.filter(status=3).order_by('-date')[:25]

    ctx = {
        'pending': productions_pending,
        'during': productions_during,
        'done': productions_done,
    }
   
    return render(request, 'production/home.html', ctx)


@staff_or_404
def ProductionStatus(request, id):
    production = Production.objects.get(id=id)
    productionOrder = ProductionOrder.objects.get(id=production.id)

    if request.method == 'POST':
        production.status = 3
        production.save()
        productionOrder.status = 3
        productionOrder.save()

        return redirect('detail-production', id=production.id)



def CreateProduction(request, id):
    productionOrder = ProductionOrder.objects.get(id=id)
    productionOrder.status = 1
    productionOrder.save()
    #user_id = request.user.id
    production, created = Production.objects.get_or_create(
        id=productionOrder.id,
        customer=productionOrder.customer,
        #user_id=user_id,
        order=productionOrder.order,
        date=productionOrder.date, )

    mats = production.productionmaterial_set.all()

    duplicates = productionOrder.materialservices_set.values("material").annotate(area_sum=Sum("area"))

    for materials in duplicates:
        data = []

        for keys, values in materials.items():
            data.append(values)
        if None in data:
            pass
        else:
            mats.create(production_id=production.id,
                        material_id=data[0],
                        area=data[1])

    return redirect('edit-production', id=production.id)


@staff_or_404
def EditProduction(request, id):
    productionOrder = ProductionOrder.objects.get(id=id)
    

    try:
        production = Production.objects.get(id=id)
        if production.status == 1:
            production.user_id = request.user.id
            production.status = 2
            production.save()
            productionOrder.status = 2
            productionOrder.save()
    except Production.DoesNotExist:
        return redirect('stock')

    materials = production.productionmaterial_set.all()

    ctx = {
        'order': productionOrder,
        'production': production,
        'materials': materials,
    }

    return render(request, 'production/edit_production.html', ctx)


@staff_or_404
def DetailProduction(request, id):
    production = Production.objects.get(id=id)
    productionOrder = ProductionOrder.objects.get(id=id)
    materials = production.productionmaterial_set.all()

    ctx = {
        'order': productionOrder,
        'production': production,
        'materials': materials,
    }

    return render(request, 'production/detail_production.html', ctx)


@staff_or_404
def ProductionMaterialIncrement(request, id):
    productionMaterial = ProductionMaterial.objects.get(id=id)
    material = Material.objects.get(id=productionMaterial.material.id)
    productionMaterial.quantity += 1
    productionMaterial.save()
    material.quantity -= 1
    material.save()

    return redirect('edit-production', id=productionMaterial.production.id)


@staff_or_404
def ProductionMaterialDecrement(request, id):
    productionMaterial = ProductionMaterial.objects.get(id=id)
    material = Material.objects.get(id=productionMaterial.material.id)
    productionMaterial.quantity -= 1
    productionMaterial.save()
    material.quantity += 1
    material.save()

    return redirect('edit-production', id=productionMaterial.production.id)


@staff_or_404
def ProductionComments(request, id):
    productionMaterial = ProductionMaterial.objects.get(id=id)
    comments = productionMaterial.comments.all()
    form = ProductionCommentsForm()

    if request.method == 'POST':
        form = ProductionCommentsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.comment = request.POST['comment']
            obj.productionMaterial = productionMaterial
            obj.save()

            return redirect('edit-production',
                            id=productionMaterial.production.id)

    ctx = {
        'productionMaterial': productionMaterial,
        'form': form,
    }

    return render(request, 'production/comments.html', ctx)


@staff_or_404
def ProductionStockFilter(request, id):
    productionMaterial = ProductionMaterial.objects.get(id=id)
    productionStocks = productionMaterial.stocks.all()

    f = StockFilter(
        request.GET,
        queryset=Stock.objects.filter(material=productionMaterial.material)
    )

    ctx = {
        'material': productionMaterial,
        'stocks': productionStocks,
        'filter': f,
    }

    return render(request, 'stock/produciton_stock_filter.html', ctx)


@staff_or_404
def ProductionStockIn(request, id):
    productionMaterial = ProductionMaterial.objects.get(id=id)
    stock = Stock.objects.filter(length=0, width=0).first()
    form = StockCreateInForm()

    if request.method == 'POST':
        form = StockCreateInForm(request.POST)
        if form.is_valid():
            form = StockCreateInForm(request.POST)
            form.save(commit=False)
            if stock is None:
                newStock = Stock.objects.create(
                    length=request.POST['length'],
                    width=request.POST['width'],
                    material=productionMaterial.material,
                )

                productionMaterial.productionstockin_set.create(
                    number=newStock.id,
                    length=request.POST['length'],
                    width=request.POST['width'],
                    material=productionMaterial.material)
            else:
                stock.length = request.POST['length']
                stock.width = request.POST['width']
                stock.material = productionMaterial.material
                stock.save()
                productionMaterial.productionstockin_set.create(
                    number=stock.id,
                    length=request.POST['length'],
                    width=request.POST['width'],
                    material=productionMaterial.material)

            return redirect('edit-production',
                            id=productionMaterial.production_id)

    ctx = {
        'form': form,
        'material': productionMaterial,
    }

    return render(request, 'stock/create_stock.html', ctx)


def HomeOrders(request):
    orders_preparation = ProductionOrder.objects.filter(status=0).order_by('-date')[:25]
    orders_pending = ProductionOrder.objects.filter(status=1).order_by('-date')[:25]
    orders_during = ProductionOrder.objects.filter(status=2).order_by('-date')[:25]
    orders_done = ProductionOrder.objects.filter(status=3).order_by('-date')[:25]

    ctx = {
        'preparation': orders_preparation,
        'pending': orders_pending,
        'during': orders_during,
        'done': orders_done,
    }

    return render(request, 'production/orders.html', ctx)


@staff_or_404
def CreateOrder(request):
    form = CreateOrderForm()

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('edit-order', id=obj.id)

    return render(request, 'production/create_order.html', {'form': form, })


@staff_or_404
def EditOrder(request, id):
    order = ProductionOrder.objects.get(id=id)
    ms = order.materialservices_set.all()
    form = EditOrderForm()
    comment = CommentForm()
    attachment = AttachmentForm()

    if request.method == 'POST' and 'add' in request.POST:
        form = EditOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.productionorder_id = order.id
            obj.save()

            return redirect('edit-order', id=order.id)
        else:
            form = EditOrderForm()

    if request.method == 'POST' and 'done' in request.POST:
        order.status = 1
        order.save()
        CreateProduction(request.POST, order.id)
        return redirect('detail-order', id=order.id)

    if request.method == 'POST' and 'comment' in request.POST:
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment.instance.user = request.user
            comment.instance.order = order
            comment.save()

        return redirect('edit-order', id=order.id)

    if request.method == 'POST' and 'file' in request.POST:
        attachment = AttachmentForm(request.POST, request.FILES)
        if attachment.is_valid():
            attachment.instance.production_order_id = order.id
            attachment.save()

        return redirect('edit-order', id=order.id)

    if request.method == 'POST' and 'delete' in request.POST:
        obj = MaterialServices.objects.get(id=request.POST['ms_id'])
        obj.delete()
        return redirect('edit-order', id=order.id)

    ctx = {
        'order': order,
        'materialservices': ms,
        'form': form,
        'comment': comment,
        'attachment': attachment,
    }

    return render(request, 'production/edit_order.html', ctx)


@staff_or_404
def DetailOrder(request, id):
    order = ProductionOrder.objects.get(id=id)
    ms = order.materialservices_set.all()

    if order.status == 0:
        return redirect('edit-order', id=order.id)

    ctx = {
        'order': order,
        'materialservices': ms,
    }

    return render(request, 'production/detail_order.html', ctx)


class OrderDescription(UpdateView):
    model = ProductionOrder
    template_name = "stock/create_object.html"
    fields = ['description']

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('edit-order'))


def mail(request, id):
    order = ProductionOrder.objects.get(id=id)

    ctx = {
        'name': order.customer,
        'status': order.get_status_display,
    }

    template = render_to_string('production/email_template.html', ctx)
    subject, from_email, to = 'Zamówienie nr {} - status: {}'.format(order.order,
                                                                     order.get_status_display()), settings.EMAIL_HOST_USER, order.customer.email
    text_content = 'Test test test.'
    html_content = render_to_string('production/email_template.html', ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect('detail-order', id=order.id)


class SearchOrder(ListView):
    model = ProductionOrder
    paginate_by = 100
    template_name = 'production/search_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductionOrderFilter(self.request.GET, queryset=self.get_queryset())
        print(ProductionOrderFilter(self.request.GET, queryset=self.get_queryset()))
        return context
