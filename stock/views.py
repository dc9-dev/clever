from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

from .filters import StockFilter
from .forms import ProductionForm, StockCreateForm
from .models import Stock, Material, Production, ProductionStock, Cutter


class StockView(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET, queryset=self.get_queryset()),
            'materials': Material.objects.all().order_by('name'),
            'productioins': Production.objects.all().order_by('-date'),
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

def TakeStock(request, id):
    
    stock = Stock.objects.get(id=id)
    stock.width = 0
    stock.length = 0
    stock.save()

    return redirect('stock')

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

def CreateProduction(request):

    user = request.user
    user_id = request.user.id

    if request.method == 'POST':
        production = Production.objects.create(user_id=user_id, order=request.POST['title'])

        return redirect('edit-production', id=production.id)

    return render(request, 'stock/create_production.html', {})


def EditProduction(request, id):
    
    production = Production.objects.get(id=id)
    #stocks = production.stocks.all()
    productionStocks = production.productionStocks.all()
    
    form = ProductionForm()

    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            
            material = Material.objects.get(id=request.POST['material'])
            material.quantity -= int(request.POST['materialUsed'])
            material.save()

            stocks = form.cleaned_data['stocks']

            # for stock in stocks:
            #     productionStock = ProductionStock.objects.create(
            #         width=stock.width,
            #         length=stock.length,
            #         material=stock.material.short_name,
            #         )
            #     productionStock.production.add(production)

               

            #stocks = request.POST.getlist['stocks']
            # print(stocks)

            # for stock in stocks:


                # production.productionStocks.create(
                #         width=stock.width,
                #         length=stock.length,
                #         material=stock.material.short_name)
               

            form.save()

            return redirect('edit-production', id=id)
        else:
            form = ProductionForm()
            return redirect('edit-production', id=id) 


    context = {
        'form': form,
        # 'stocks': stocks,
        'production': production,
        'productionStocks': productionStocks,
    }
    return render(request, 'stock/edit_production.html', context)


def DetailProduction(request, id):

    production = Production.objects.get(id=id)
    stocks = production.stocks.all()

    context = {
        'production': production,
        'stocks': stocks,
    }
    return render(request, 'stock/detail_production.html', context)