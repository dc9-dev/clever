from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

from .filters import StockFilter
from .forms import ProductionForm
from .models import Stock, Material, Production, ProductionStock


class Stock(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET, queryset=self.get_queryset()),
            'materials': Material.objects.all().order_by('name'),
            'productioins': Production.objects.all().order_by('-date'),
            })
        return context


def CreateProduction(request):

    user = request.user
    user_id = request.user.id

    if request.method == 'POST':
        production = Production.objects.create(user_id=user_id, order=request.POST['title'])

        return redirect('edit-production', id=production.id)

    return render(request, 'stock/create_production.html', {})


def EditProduction(request, id):
    
    production = Production.objects.get(id=id)
    stocks = production.stocks.all()
    productionStocks = production.productionStocks.all()
    
    form = ProductionForm()

    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            
            material = Material.objects.get(id=request.POST['material'])
            material.quantity -= int(request.POST['materialUsed'])
            material.save()
            
            for stock in production.stocks.all():
                stock.width = 0
                stock.length = 0
                stock.material.short_name = ""
                stock.save
                print(stock)
# for stock in production.stocks.all():
#     ...:     production.productionStocks.create(
#     ...:         width=stock.width,
#     ...:         length=stock.length,
#     ...:         material=stock.material.short_name,
#     ...:     )
            form.save()

            return redirect('edit-production', id=id)
        else:
            form = ProductionForm()
            return redirect('edit-production', id=id) 


    context = {
        'form': form,
        'stocks': stocks,
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