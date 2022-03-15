import re
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from .filters import StockFilter, GrnFilter
from .forms import StockCreateForm, grnCreateForm, GRNMaterailForm, CreateMaterialForm, CreateServicesForm, CreateContractorForm
from production.models import ProductionMaterial, Services
from .models import Contractor, Stock, Material, Cutter, GoodsReceivedNote, Cash


class StockView(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET,
                                  queryset=self.get_queryset()),
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


def GRN(request):

    grns = GoodsReceivedNote.objects.all().order_by('-date')
    filter = GrnFilter(request.GET, queryset=grns)
    form = grnCreateForm()

    if request.method == 'POST':
        form = grnCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('edit-grn', id=obj.id)
        else:
            form = grnCreateForm()

    ctx = {
        'grns': grns,
        'filter': filter,
        'form': form,
        }

    return render(request, 'stock/grn.html', ctx)


def EditGRN(request, id):

    grn = GoodsReceivedNote.objects.get(id=id)
    materials = grn.grnmaterial_set.all()
    form = GRNMaterailForm()

    if request.method == 'POST':
        if 'addMaterial' in request.POST:
            form = GRNMaterailForm(request.POST)
            print(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)

                if int(float(request.POST['area']) * 1000) % int(float(obj.material.material_area ) * 1000 ) == 0:

                    material = Material.objects.get(id=request.POST['material'])
                    material.quantity += float(request.POST['area']) / float(material.material_area)
                    material.save()

                    obj.grn = grn
                    obj.save()

                    return redirect('edit-grn', id=grn.id)

                else:
                    error = "Wprowadziłeś ilość materiału równą {}m2.<br>\
                            Jedna płyta ma powierzchnie {}m2<br>\
                            Nie wychodzą równe sztuki płyt, wróć do PZtki i popraw metry  ".format(request.POST['area'], obj.material.material_area)
                    return HttpResponse(error)
        else:
            form = GRNMaterailForm()
        
        if 'checked' in request.POST:
            grn.status = 1
            grn.save()
            return redirect('detail-grn', id=grn.id)

    ctx = {
        'grn': grn,
        'form': form,
        'materials': materials,
        }

    return render(request, 'stock/edit_grn.html', ctx)


def DetailGRN(request, id):

    grns = GoodsReceivedNote.objects.all().order_by('date')
    grn = GoodsReceivedNote.objects.get(id=id)
    materials = grn.grnmaterial_set.all()

    if request.method == 'POST':
        grn.status = 1
        grn.save()
        return redirect('detail-grn', grn.id)

    ctx = {
        'grns': grns,
        'grn': grn,
        'materials': materials,
        }

    return render(request, 'stock/detail_grn.html', ctx)


def check_grn(request, id):

    grn = GoodsReceivedNote.objects.get(id=id)

    if request.method == 'POST':
        grn.status = 1
        grn.save()
        return redirect('detail-grn', id=grn.id)
    

def cash(request):
    cashes = Cash.objects.all()
    ctx = {
        'cashes': cashes,
    }

    return render(request, 'stock/home_cash.html', ctx)


class MaterialCreateView(CreateView):
    model = Material
    template_name = "stock/create_object.html"
    success_url = '/'
    form_class = CreateMaterialForm


class ServicesCreateView(CreateView):
    model = Services
    template_name = "stock/create_object.html"
    success_url = '/'
    form_class = CreateServicesForm


class ContractorCreateView(CreateView):
    model = Contractor
    template_name = "stock/create_object.html"
    success_url = reverse_lazy('grn')
    form_class = CreateContractorForm
