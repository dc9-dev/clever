import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, response
from django.shortcuts import redirect, render
from .models import Order, Item
from .forms import ItemForm
from account.models import UserBase

@login_required(login_url='login')
def home(request):

    user_id = request.user.id
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user_id=user_id)[0:10]
    
    orders_total = Order.objects.filter(user_id=user_id).count()
    orders_pending = Order.objects.filter(user_id=user_id, status='0').count()
    orders_during = Order.objects.filter(user_id=user_id, status='1').count()
    orders_done = Order.objects.filter(user_id=user_id, status='2').count()

    context = { 'orders': orders,
                'orders_total': orders_total,
                'orders_pending': orders_pending,
                'orders_during': orders_during,
                'orders_done': orders_done,
                }
    return render(request, "order/home.html", context)


def new(request):
    user_id = request.user.id
    order = Order.objects.create(user_id=user_id)

    return redirect('edit', slug=order.slug)

def detail(request, slug):
    order = Order.objects.get(slug=slug)
    item = order.item_set.all()
    context = {
        'order': order,
        'item': item,
    }

    return render(request, 'order/detail.html', context)

def edit(request, slug):
    order = Order.objects.get(slug=slug)
    item = order.item_set.all()
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form = ItemForm(request.POST)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.order = order
            obj.save()
            form = ItemForm()
            return redirect('edit', slug=slug)
        else:
            form = ItemForm()
            return redirect('edit', slug=slug)
         
    context = {
        'order': order,
        'item': item,
        'form': form,
    }
    return render(request, "order/edit.html", context)


def export_csv(request, slug):
    
    order = Order.objects.get(slug=slug)
    items = order.item_set.all()
 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=zamID#{}.csv'.format(order.slug)
    

    writer = csv.writer(response)

    
    
    # Add column headings to the csv file
    writer.writerow(['Długość', 'Szerokość', 'Ilość', 'Opis', 'Okleina'])

    # Loop Thu and output
    for i in items:
        writer.writerow([i.lenght, i.width, i.quantity, , i. description, i.lenght1, i.lenght2, i.width1, i.width2])

    return response