from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

from .filters import StockFilter
from .forms import StockCreateForm, ProductionMaterialForm, StockCreateInForm, ProductionCommentsForm
from .models import Stock, Material, Production, ProductionStock, ProductionMaterial, ProductionComments, Cutter



class StockView(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET, queryset=self.get_queryset()),
            'materials': Material.objects.all().order_by('name'),
            'cutters': Cutter.objects.all().order_by('-name'),
            })
        return context

class CreateStock(CreateView):

    def get(self, request, *args, **kwargs):

        context = {'form': StockCreateForm()}
        return render(request, 'stock/create_stock.html', context)

    def post(self, request, *args, **kwargs):

        form = StockCreateForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('stock')

        for index, i in enumerate(Stock.objects.all()):
            i.id = index + 1
            i.save()

        return render(request, 'stock/create_stock.html', {'form': form})

def TakeStock(request, id1, id2):
    
    productionMaterial = ProductionMaterial.objects.get(id=id1)
    stock = Stock.objects.get(id=id2)

    productionStocks = productionMaterial.stocks.update_or_create(
        number=id2,
        length=stock.length,
        width=stock.width,
        material=stock.material,
        )

    stock.width = 0
    stock.length = 0
    stock.save()

    return redirect('edit-production', productionMaterial.production.id )

def AddStock(request, id):

    stock = Stock.objects.get(id=id)
    form = StockCreateForm()

    if request.method == 'POST':
        form = StockCreateForm(request.POST)
        if form.is_valid():
            form = StockCreateForm(request.POST)
            form.save(commit=False)
            stock.width = request.POST['width']
            stock.length = request.POST['length']
            stock.material.id = request.POST['material']
            stock.save()
            return redirect('stock')

    return render(request, 'stock/create_stock.html', {'form': form})


def CutterSharp(request, id):

    cutter = Cutter.objects.get(id=id)

    return redirect('stock')

def CutterBuy(request, id):

    cutter = Cutter.objects.get(id=id)

def ProductionHome(request):

    productions = Production.objects.all().order_by('-date')

    ctx = {'productions': productions,}
      
    return render(request, 'production/home.html', ctx)

def ProductionStatus(request, id):

    production = Production.objects.get(id=id)\
    
    if request.method == 'POST':
        production.status = 1
        production.save()
        return redirect('detail-production', id=production.id)


def CreateProduction(request):

    user = request.user
    user_id = request.user.id

    if request.method == 'POST':
        production = Production.objects.create(user_id=user_id, order=request.POST['title'])

        return redirect('edit-production', id=production.id)

    return render(request, 'stock/create_production.html', {})


def EditProduction(request, id):

    production = Production.objects.get(id=id)
    materials = production.productionmaterial_set.all()
    #comments = ProductionComments.objects.filter(productionMaterials)
    materialForm = ProductionMaterialForm()
    commentsForm = ProductionCommentsForm()

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

    ctx = {

        'production': production,
        'materials': materials,
        'materialForm': materialForm,
        'comments': commentsForm,
        #'comments': comments,
    }

    return render(request, 'stock/edit_production.html', ctx)


def ProductionStockFilter(request, id):

    productionMaterial = ProductionMaterial.objects.get(id=id)
    productionStocks = productionMaterial.stocks.all()

    f = StockFilter(request.GET, queryset=Stock.objects.filter(material=productionMaterial.material))

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

                productionMaterial.productionstockin_set.create(number=newStock.id,
                                                                length=request.POST['length'],
                                                                width=request.POST['width'],
                                                                material=productionMaterial.material)
            else:
                stock.length = request.POST['length']
                stock.width = request.POST['width']
                stock.material = productionMaterial.material
                stock.save()
                productionMaterial.productionstockin_set.create(number=stock.id, 
                                                                length=request.POST['length'],
                                                                width=request.POST['width'],
                                                                material=productionMaterial.material)

            return redirect('edit-production', id=productionMaterial.production_id)

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