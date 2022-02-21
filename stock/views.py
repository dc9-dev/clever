from django.http import HttpResponse, FileResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter


from datetime import datetime 


from .filters import StockFilter
from .forms import StockCreateForm, ProductionMaterialForm, StockCreateInForm, ProductionCommentsForm, grnForm
from .models import Stock, Material, Production, ProductionStock, ProductionMaterial, ProductionComments, Cutter, GoodsReceivedNote


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

    production = Production.objects.get(id=id)
    
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

            return redirect('edit-production', id=productionMaterial.production.id)

    ctx = {
        'productionMaterial': productionMaterial,
        'form': form,
    }

    return render(request, 'production/comments.html', ctx)
        

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


def ProductionRaport(request):
    pass
#     today = datetime.today()
#     productions = Production.objects.all()#filter(date__date=today)

#     response = HttpResponse(content_type='application/pdf')
    
#     filename = 'pdf_demo' + today.strftime('%Y-%m-%d') + '.pdf'
#     #response['Content-Disposition'] = 'attachement; filename={}.pdf'.format(filename)

#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

#     textob = c.beginText()
#     textob.setTextOrigin(cm, cm)
#     textob.setFont("Helvetica",15)
    
#     lines = []

#     for production in productions:
#         lines.append(production.order)
#         lines.append(" ")

#     for line in lines:
#         textob.textLine(line)

#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buffer.seek(0)

#     return FileResponse(buffer, as_attachment=True, filename=filename)


#     # for production in productions:
#     #     p.setFont("Helvetica",15,leading=None)
#     #     p.drawString(x1,y1-12,production.order)

#     # p.setTitle("Raport")
#     # p.showPage()
#     # p.save()

#     # pdf = buffer.getvalue()
#     # buffer.close()
#     # response.write(pdf)

#     return response


def GRN(request):

    grns = GoodsReceivedNote.objects.all()
    form = grnForm()

    if request.method == 'POST':
        form = grnForm(request.POST)
        if form.is_valid():
            print(request.POST)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('home')
        else:
            form = grnForm()

    ctx = {'grns': grns,
           'form': form,}
    
    return render(request, 'production/grn.html', ctx)
