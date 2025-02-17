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
from .models import (MaterialServices,
                     Production,
                     ProductionMaterial,
                     ProductionOrder,
                     )
from .filters import ProductionOrderFilter

from clever.decorators import staff_or_404
from stock.models import Stock
from stock.forms import StockCreateInForm
from stock.filters import StockFilter
from stock.models import Material, Gender
from datetime import datetime
from account.models import UserBase

def load_materials(request):
    # print("loading materials in production")
    gender_id = request.GET.get('gender')
    materials = Material.objects.all().filter(gender_id=int(gender_id)).order_by('name')
    # print(materials)
    return render(request, 'production/material_dropdown_list_options.html', {'materials': materials})

@staff_or_404
def ProductionHome(request):

    productions_pending = Production.objects.filter(
        status=1).order_by('date')[:1000]
    all_frezers_ids = Production.objects.filter(
        status__gte=1).values_list('user_id', flat=True).distinct()
    all_frezers = []
    frezers = []
    for frezer in all_frezers_ids:
        if frezer == None:
            continue
        if  frezer < 7:
            continue
        
        f = {}
        
        user = UserBase.objects.get(id=frezer)
        f["user"] = user
        
        productions_during_by_frezer = Production.objects.filter(
            status=2, user_id=frezer).order_by('date')[:1000]
        f["during"] = productions_during_by_frezer
        
        done = Production.objects.filter(
            status=3, user_id=frezer).order_by('date')[:1000]

        tmp = {}
        tmp_rest = []
        for p in done:
            if p.updated_at:
                day = p.updated_at.strftime("%d")
                month = p.updated_at.strftime("%m")
                year = p.updated_at.strftime("%Y")
                short_date = f"{day}-{month}-{year}"
                if short_date in tmp.keys():
                    tmp[short_date].append(p)
                else:
                    tmp[short_date] = [p]
            else:
                tmp_rest.append(p)
                
        tmp = dict(reversed(sorted(tmp.items(), key=lambda item: datetime.strptime(item[0], '%d-%m-%Y'))))
        tmp["reszta"] = tmp_rest
        f["done"] = tmp
        frezers.append(f)
        
    # not needed anymore
    productions_during = Production.objects.filter(
        status=2).order_by('date')
    productions_done = Production.objects.filter(
        status=3).order_by('date')[:25]
        
    ctx = {
        'pending': productions_pending,
        'during': productions_during,
        'during_by_frezer': productions_during_by_frezer,
        'done': productions_done,
        # 'done_by_frezer': productions_done_by_frezer,
        'all_frezers' : all_frezers,
        'frezers' : frezers
    }

    return render(request, 'production/home.html', ctx)


@staff_or_404
def ProductionStatus(request, id):
    production = Production.objects.get(id=id)
    productionOrder = ProductionOrder.objects.get(id=production.id)

    if request.method == 'POST':
        production.status = 3
        production.updated_at = datetime.now()
        production.save()
        productionOrder.status = 3
        productionOrder.updated_at = datetime.now()
        productionOrder.save()

        return redirect('detail-production', id=production.id)


def CreateProduction(request, id):
    productionOrder = ProductionOrder.objects.get(id=id)
    productionOrder.status = 1
    productionOrder.updated_at = datetime.now()
    productionOrder.save()
    # user_id = request.user.id

    try:
        old_production = Production.objects.get(id=productionOrder.id)
        old_production.delete()
    except Exception as e:
        print(e)

    production, created = Production.objects.update_or_create(
        id=productionOrder.id,
        customer=productionOrder.customer,
        # user_id=user_id,
        order=productionOrder.order,
        date=productionOrder.date, )

    mats = production.productionmaterial_set.all()

    duplicates = productionOrder.materialservices_set.values(
        "material").annotate(area_sum=Sum("area"))

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
            production.updated_at = datetime.now()
            production.save()
            productionOrder.status = 2
            productionOrder.updated_at = datetime.now()
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
def DeleteProduction(request, id):
    production = Production.objects.get(id=id)
    production.delete()
    productionOrder = ProductionOrder.objects.get(id=id)
    productionOrder.delete()

    return redirect('home-production')


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


class ProductionLabel(UpdateView):
    model = Production
    fields = ['comments']
    template_name = "production/label.html"

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('edit-production'))


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
        form = StockCreateInForm(request.POST, initial={'gender' : productionMaterial.material.gender.id})
        # print(form.errors)
        if form.is_valid():
            print("form is valid")
            # get longer side
            length = int(request.POST['length'])
            width = int(request.POST['width'])
            longer_side = int(
                max([length, width]))
            # print(f"longer side: {longer_side}")
            
            # assign rack
            if longer_side < 1500:
                rack = 'A'
            else:
                rack = 'B'

            # print(f"rack: {rack}")
            if stock is None:
                newStock = Stock.objects.create(
                    length=length,
                    width=width,
                    material=productionMaterial.material,
                    created_by=f'{request.user.first_name[0]}{request.user.last_name[0]}',
                    rack=rack,
                    gender_id = productionMaterial.material.gender.id
                )

                productionMaterial.productionstockin_set.create(
                    number=newStock.id,
                    length=length,
                    width=width,
                    material=productionMaterial.material)

                all_stocks_on_rack = Stock.objects.all().filter(rack=newStock.rack)
                new_rack_id = 1

                # if no stocks yet create stock with id 1
                if len(all_stocks_on_rack) == 0:
                    print('adding first stock')
                    newStock.rack_id = 1
                    newStock.save()
                else:
                    print('at least 1 stock in db, adding more')
                    # get first free id between 1 and 100
                    all_stocks_on_rack = Stock.objects.all().filter(
                        rack=newStock.rack, gender_id=productionMaterial.material.gender.id).order_by('rack_id')
                    for i in all_stocks_on_rack:
                        print(f'checking stock with id: {i.rack_id}')
                        if new_rack_id != i.rack_id:
                            # found first empy id, create stock with that id
                            newStock.rack_id = new_rack_id
                            newStock.save()
                            break
                        new_rack_id += 1

                    # all ids taken between first and last stock, add new stock at 'the end'
                    newStock.rack_id = new_rack_id
                    newStock.save()
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
        'gender': productionMaterial.material.gender,
        'material': productionMaterial,
    }

    return render(request, 'stock/create_stock.html', ctx)


def HomeOrders(request):
    orders_preparation = ProductionOrder.objects.filter(
        status=0).order_by('-date')[:100]
    orders_pending = ProductionOrder.objects.filter(
        status=1).order_by('-date')[:100]
    orders_during = ProductionOrder.objects.filter(
        status=2).order_by('-date')[:100]
    orders_done = ProductionOrder.objects.filter(
        status=3).order_by('-date')[:100]

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
            # print(f'user: {request.user.id}')
            obj.user_id = request.user.id
            obj.save()
            return redirect('edit-order', id=obj.id)

    return render(request, 'production/create_order.html', {'form': form, })


@staff_or_404
def DeleteOrder(request, id):
    if request.method == 'POST' and 'delete' in request.POST:
        obj = ProductionOrder.objects.get(id=id)
        obj.delete()

    return redirect('home-orders')


@staff_or_404
def EditOrder(request, id):
    order = ProductionOrder.objects.get(id=id)
    ms = order.materialservices_set.all()
    form = EditOrderForm()
    comment = CommentForm()
    attachment = AttachmentForm()

    if request.method == 'POST' and 'add' in request.POST:
        form = EditOrderForm(request.POST)
        print("elo from")
        print(f'form: {form}')
        print(f"form is valid: {form.cleaned_data}")
        if form.is_valid():
            obj = form.save(commit=False)
            obj.productionorder_id = order.id
            obj.save()

            return redirect('edit-order', id=order.id)
        else:
            form = EditOrderForm()

    if request.method == 'POST' and 'done' in request.POST:
        order.status = 1
        order.updated_at = datetime.now()
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
        'genders': Gender.objects.all(),
    }

    return render(request, 'production/edit_order.html', ctx)


@staff_or_404
def DetailOrder(request, id):
    order = ProductionOrder.objects.get(id=id)
    production = None
    frezer = None
    try:
        production = Production.objects.get(order=order.order)
        try:
            frezer = UserBase.objects.get(id=production.user_id)
        except UserBase.DoesNotExist:
            pass

    except Production.DoesNotExist:
        pass
    ms = order.materialservices_set.all()

    if order.status == 0:
        return redirect('edit-order', id=order.id)

    ctx = {
        'order': order,
        'materialservices': ms,
        'frezer' : frezer
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
        context['filter'] = ProductionOrderFilter(
            self.request.GET, queryset=self.get_queryset())
        print(ProductionOrderFilter(self.request.GET, queryset=self.get_queryset()))
        return context
