from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Stock
from .filters import StockFilter

@staff_member_required
def stock(request):
    
    stock = Stock.objects.all()
    
    myFilter = StockFilter(request.GET, queryset=stock)
    stock = myFilter.qs 

    context = {
        'stock': stock,
        'myFilter': myFilter,
    }
    return render(request, 'stock/home.html', context)

@staff_member_required
def stock_take(request, stock_id):

    stock = Stock.objects.filter(stock_id=stock_id)
    stock.update(width=0, length=0, material=1)

    return redirect('stock')


    return render(request, 'stock/search.html', {})

