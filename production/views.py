from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .forms import (ProductionMaterialForm,
                    ProductionCommentsForm,
                    CreateOrderForm)
from .models import (Production,
                     ProductionStock,
                     ProductionMaterial,
                     ProductionComments,
                     ProductionOrder)


def ProductionHome(request):

    productions = Production.objects.all().order_by('-date')

    ctx = {'productions': productions, }

    return render(request, 'production/home.html', ctx)


def ProductionStatus(request, id):

    production = Production.objects.get(id=id)

    if request.method == 'POST':
        production.status = 1
        production.save()

        return redirect('detail-production', id=production.id)


def CreateProduction(request):

    user = request.user
    user_id = request.user.id

    if request.method == 'POST':
        production = Production.objects.create(user_id=user_id,
                                               order=request.POST['title'])

        return redirect('edit-production', id=production.id)

    return render(request, 'stock/create_production.html', {})


def EditProduction(request, id):

    try:
        production = Production.objects.get(id=id)
    except Production.DoesNotExist:
        return redirect('stock')

    materials = production.productionmaterial_set.all()
    materialForm = ProductionMaterialForm()

    if request.method == 'POST':
        materialForm = ProductionMaterialForm(request.POST)
        if materialForm.is_valid():
            obj = materialForm.save(commit=False)
            obj.production = production
            obj.save()

            material = Material.objects.get(id=request.POST['material'])
            material.quantity -= int(request.POST['quantity'])
            material.save()

            return redirect('edit-production', id=production.id)
        else:
            materialForm = ProductionMaterialForm()

    ctx = {

        'production': production,
        'materials': materials,
        'materialForm': materialForm,

    }

    return render(request, 'stock/edit_production.html', ctx)


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


def DetailProduction(request, id):

    production = Production.objects.get(id=id)
    materials = production.productionmaterial_set.all()

    ctx = {
        'production': production,
        'materials': materials,
    }

    return render(request, 'stock/detail_production.html', ctx)


def HomeOrders(request):

    orders = ProductionOrder.objects.all().order_by('-date')

    return render(request, 'production/orders.html', {'orders': orders, })


def CreateOrder(request):

    form = CreateOrderForm()

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('edit-order', id=obj.id)

    return render(request, 'production/create_order.html', {'form': form, })


def EditOrder(request, id):

    order = ProductionOrder.objects.get(id=id)
    ms = order.materialservices_set.all()
    #total = order.materialservices_set.annotate(total_price=Sum('total'))

    ctx = {
        'order': order,
        'materialservices': ms,
    }

    return render(request, 'production/edit_order.html', ctx)
