from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

from .filters import StockFilter
from .forms import ProductionForm
from .models import Stock, Material, Production, Formatka, Spad


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
    formatka = production.formatka_set.all()
    spad = production.spad_set.all()
    form = ProductionForm()

    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            print(request.POST)
            for stock in request.POST['stocks']:
                print("test")
                print(stock)
            print(request.POST['stocks'])
            material = Material.objects.get(id=request.POST['material'])
            material.quantity -= int(request.POST['materialUsed'])
            material.save()

            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            # for stock in addstocks:
            #     production.stocks.add(stock)


            return redirect('edit-production', id=id)
        else:
            form = ProductionForm()
            return redirect('edit-production', id=id) 


    context = {
        'form': form,
        'stocks': stocks,
        'formatka': formatka,
        'spad': spad,
        'production': production,
    }
    return render(request, 'stock/edit_production.html', context)


def DetailProduction(request, id):

    production = Production.objects.get(id=id)
    materials = production.materials.all()
    stocks = production.stocks.all()

    context = {
        'production': production,
        'materials': materials,
        'stocks': stocks,
    }
    return render(request, 'stock/detail_production.html', context)