from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView
                                 )
from offer.forms import CreateOfferForm, OfferItemForm, NoteForm
from .models import Offer, OfferItem


class HomeOffer(ListView):
    model = Offer
    template_name = 'offer/home.html'
    ordering = ['-date']


class CreateOfferView(CreateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'offer/create_offer.html'
    
    def get_success_url(self):
        return reverse_lazy('edit-offer', kwargs={'id': self.object.id})


def edit_offer(request, id):
    offer = Offer.objects.get(id=id)
    items = offer.offeritem_set.all()
    form = OfferItemForm()
    note = NoteForm()

    if request.method == 'POST':
        form = OfferItemForm(request.POST)
        if form.is_valid():
            form = OfferItemForm(request.POST)
            obj = form.save(commit=False)
            obj.offer_id = offer.id
            obj.save()
            return redirect('edit-offer', offer.id)
        else:
            form = OfferItemForm()
    
    if request.method == 'POST' and 'delete' in request.POST:
        obj = OfferItem.objects.get(id=request.POST['item_id'])
        obj.delete()
        return redirect('edit-offer', id=offer.id)

    if request.method == 'POST' and 'note' in request.POST:
        note = NoteForm(request.POST)
        if note.is_valid():
            note.instance.user = request.user
            note.instance.offer = offer
            note.save()

        return redirect('edit-offer', id=offer.id)
            
    print(form.errors)
    ctx = {
        'offer': offer,
        'items': items,
        'form': form,
        'note': note,
    }
    return render(request, 'offer/update_offer.html', ctx)


class OfferDetailView(DetailView):
    model = Offer
    template_name = 'offer/detail_offer.html'

