import csv
import math
from datetime import datetime
from io import BytesIO
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, response
from django.template.loader import get_template
from django.shortcuts import redirect, render
from xhtml2pdf import pisa
from django.views import View
from django.db.models import Sum
from .models import Order, Item
from .forms import ItemForm, AttachmentForm
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

    context = {
        'orders': orders,
        'orders_total': orders_total,
        'orders_pending': orders_pending,
        'orders_during': orders_during,
        'orders_done': orders_done,
}

    return render(request, "order/home.html", context)

@login_required(login_url='login')
def new(request):
    user = request.user
    user_id = request.user.id
    order = Order.objects.create(user_id=user_id)
    dt = datetime.now()
    order.title = "{}_{}".format(dt.strftime('%d_%m_%y'), user.last_name)
    order.save()

    return redirect('edit', slug=order.slug)
@login_required(login_url='login')
def detail(request, slug):

    order = Order.objects.get(slug=slug)
    item = order.item_set.all()
    attachment = order.attachment_set.all()

    context = {
        'order': order,
        'item': item,
        'attachment': attachment,
            }

    return render(request, 'order/detail.html', context)
@login_required(login_url='login')
def edit(request, slug):

    order = Order.objects.get(slug=slug)
    item = order.item_set.all()
    attachment = order.attachment_set.all()

    form = ItemForm()
    attachmentForm = AttachmentForm()

    if request.method == 'POST':
        if request.POST.get('form_type') == 'ItemForm':
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
        elif request.POST.get('form_type') == 'AttachmentForm':
            attachment = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                
                return redirect('edit', slug=slug)
            else:
                attachment = AttachmentForm()
                return redirect('edit', slug=slug)

    for index, i in enumerate(item):
        i.item_number = index + 1
        i.save()

    context = {
        'order': order,
        'item': item,
        'form': form,
        'attachmentForm': attachmentForm,
        'attachment': attachment,

    }
    return render(request, "order/edit.html", context)


@login_required(login_url='login')
def deleteItem(request, slug, item_id):

    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('edit', slug=slug)


@login_required(login_url='login')
def export_csv(request, slug):

    order = Order.objects.get(slug=slug)
    items = order.item_set.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=zam_{}.csv'.format(order.title)
    writer = csv.writer(response)
    # Add column headings to the csv file
    #writer.writerow(['lp.', 'Długość', 'Szerokość', 'Ilość', 'Opis', 'dlugosc-1', 'szerokosc-1', 'dlugosc-2', 'szerokosc2'])

    # Loop Thu and output
    for i in items:
        writer.writerow([i.item_number, i.length, i.width, i.quantity, i.description, i.material, i.length1, i.width1, i.length2, i.width2])

    return response




def export_pdf(request, slug):

    order = Order.objects.get(slug=slug)
    items = order.item_set.all()
    items_quantity = sum(items.values_list('quantity', flat=True))
    items_width = sum(items.values_list('width', flat=True))
    items_length = sum(items.values_list('length', flat=True))
    #caluculate m2, where 1000000 is used to convert mm2 to m2
    items_area = float(round((items_width * items_length)/1000000, 2))
    panel = 5.70
    panel_sum = round(items_area / panel)
    cost = panel_sum * 180 + items_quantity * 3 

    template_path = 'pdf.html'
    context = {'order': order,
               'items': items,
               'items_quantity': items_quantity,
               'items_area': items_area,
               'panel_sum': panel_sum,
               'cost': cost,
                }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="zam_%s.pdf"' % (order.title)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

