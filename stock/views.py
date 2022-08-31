from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse, FileResponse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .filters import StockFilter, GrnFilter
from .forms import StockCreateForm, grnCreateForm, GRNMaterailForm, CreateMaterialForm, CreateServicesForm, CreateContractorForm, CommentForm, AttachmentForm
from production.models import ProductionMaterial, ProductionStockIn, Services
from .models import Contractor, Stock, Material, GoodsReceivedNote, Gender

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A8

from django.contrib import messages


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
                                  queryset=self.get_queryset().order_by('rack_id')),
        })
        return context


class CreateStock(CreateView):

    def get(self, request, *args, **kwargs):

        context = {'form': StockCreateForm()}
        return render(request, 'stock/create_stock.html', context)

    def post(self, request, *args, **kwargs):
        form = StockCreateForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.created_by = f'{request.user.first_name[0]}{request.user.last_name[0]}'
            
            # get longer side
            longer_side = max([s.length, s.width])
            
            # assign rack
            if longer_side < 1500:
                s.rack = 'A'
            else:
                s.rack = 'B'

            all_stocks_on_rack = Stock.objects.all().filter(rack=s.rack)
            new_rack_id = 1

            # if no stocks yet create stock with id 1
            if len(all_stocks_on_rack) == 0:
                print('adding first stock')
                s.rack_id = 1
                s.save()
            else:
                print('at least 1 stock in db, adding more')
                # get first free id between 1 and 100
                all_stocks_on_rack = Stock.objects.all().filter(rack=s.rack).order_by('rack_id')
                for i in all_stocks_on_rack:
                    print(f'checking stock with id: {i.rack_id}')
                    if new_rack_id != i.rack_id:
                        # found first empy id, create stock with that id
                        s.rack_id = new_rack_id
                        s.save()
                        break
                    new_rack_id += 1

                # all ids taken between first and last stock, add new stock at 'the end'
                s.rack_id = new_rack_id
                s.save()
            messages.success(request, new_rack_id)
            messages.info(request, s.id)
            return redirect('stocks')
        else:
            print(form.is_valid())
            print(form.errors)

        # not sure what this does?
        for index, i in enumerate(Stock.objects.all()):
            i.id = index + 1
            i.save()

        return render(request, 'stock/create_stock.html', {'form': form})


def DeleteStock(request, id):
    si = ProductionStockIn.objects.filter(number = id).first()
    if si:
        si.delete()

    s = Stock.objects.get(pk=id)
    rack_id = s.rack_id
    rack = s.rack
    s.delete()
    
    messages.error(request, f'Usunięteo formatkę z #ID {rack_id} z regalu {rack}')

    return redirect('stocks')


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

    return redirect('edit-production', productionMaterial.production.id)


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

                if int(float(request.POST['area']) * 1000) % int(float(obj.material.material_area) * 1000) == 0:

                    material = Material.objects.get(
                        id=request.POST['material'])
                    material.quantity += float(
                        request.POST['area']) / float(material.material_area)
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
        return reverse_lazy('detail-contractor', kwargs={'pk': self.object.pk})


class ContractorDetailView(DetailView):
    model = Contractor
    template_name = "account/detail_contractor.html"


def Generate_stock_label_not_production(request, id):
    stock = Stock.objects.get(id=id)
    buf = BytesIO()

    c = canvas.Canvas(buf, pagesize=A8, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(cm, cm)
    textob.setFont("Helvetica", 10)
    textob.textLine("")
    textob.textLine("")
    textob.textLine("{}".format(stock.material))
    textob.textLine("")
    textob.textLine("")
    textob.textLine("")
    textob.textLine("")
    textob.setFont("Helvetica", 42)
    textob.textLine("#{}".format(stock.rack_id))

    textob.setFont("Helvetica", 14)
    textob.textLine("{}x{}".format(stock.length, stock.width))
    if stock.rack:
        textob.textLine(f'Regal {stock.rack}')
    textob.textLine(stock.created_by)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='#{}.pdf'.format(stock.rack_id))
