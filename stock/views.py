from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Stock
from order.models import Material
from .filters import StockFilter


@staff_member_required
def stock(request):

    qs = Stock.objects.all()
    material = Material.objects.all()

    materials = Material.objects.all()
    stock = Stock.objects.all()

    length = request.GET.get('length')
    width = request.GET.get('width')
    material = request.GET.get('material')

    print(length, width, material)
 
 

    context = {
        'stock': stock,
        'materials': materials,
     
        
       }
    return render(request, 'stock/home.html', context)




@staff_member_required
def stock_take(request, stock_id):

    stock = Stock.objects.filter(stock_id=stock_id)
    stock.update(width=0, length=0, material=1)

    return redirect('stock')


    return render(request, 'stock/search.html', {})
