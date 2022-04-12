from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .filters import StockFilter, GrnFilter
from .forms import StockCreateForm, grnCreateForm, GRNMaterailForm, CreateMaterialForm, CreateServicesForm, CreateContractorForm, CommentForm, AttachmentForm
from production.models import ProductionMaterial, Services
from .models import Contractor, Stock, Material, GoodsReceivedNote, Gender


class WarehouseListView(ListView, LoginRequiredMixin):
    model = Gender
    template_name = 'stock/home.html'


class StockView(ListView):
    model = Stock
    template_name = 'stock/stocks.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET,
                                  queryset=self.get_queryset()),
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
            return redirect('stocks')
        else:
            print(form.is_valid())
            print(form.errors)

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
    comment = CommentForm()
    attachment = AttachmentForm()

    if request.method == 'POST':
        if 'addMaterial' in request.POST:
            form = GRNMaterailForm(request.POST)
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

    if request.method == 'POST' and 'delete' in request.POST:
        obj = grn.grnmaterial_set.get(id=request.POST['m_id'])
        obj.delete()
        return redirect('edit-grn', id=grn.id)

    if request.method == 'POST' and 'comment' in request.POST:
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment.instance.grn = grn
            comment.save()

        return redirect('edit-grn', id=grn.id)

    if request.method == 'POST' and 'file' in request.POST:
        attachment = AttachmentForm(request.POST, request.FILES)
        if attachment.is_valid():
            attachment.instance.grn_id = grn.id
            attachment.save()

        return redirect('edit-grn', id=grn.id)

    ctx = {
        'grn': grn,
        'form': form,
        'materials': materials,
        'comment': comment,
        'attachment': attachment,
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


class MaterialCreateView(CreateView):
    model = Material
    template_name = "stock/create_object.html"
    form_class = CreateMaterialForm

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('edit-order'))


class ServicesCreateView(CreateView):
    model = Services
    template_name = "stock/create_object.html"
    form_class = CreateServicesForm

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('edit-order'))


class ContractorCreateView(CreateView):
    model = Contractor
    template_name = "stock/create_object.html"
    success_url = reverse_lazy('grn')
    form_class = CreateContractorForm


class ContractorUpdateView(UpdateView):
    model = Contractor
    template_name = "account/update_contractor.html"
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('detail-contractor', kwargs = {'pk': self.object.pk })

class ContractorDetailView(DetailView):
    model = Contractor
    template_name = "account/detail_contractor.html"