from aiohttp import request
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy 
from django.http.response import JsonResponse
from .forms import CreatePaymentForm, UpdatePaymentForm
from .filters import PaymentFilter
from .models import Payment, Cash



class CashListView(ListView):
    model = Cash
    template_name = 'cash/home_cash.html'


def CashDetail(request, id):
    cash = Cash.objects.get(id=id)   
           
    ctx = {
        'cash': cash,
    }
    return render(request, 'cash/cash_detail.html', ctx)


def PaymentCreateView(request, id):
    cash = Cash.objects.get(id=id)
    form = CreatePaymentForm()

    if request.method == 'POST':
        form = CreatePaymentForm(request.POST)
        if form.is_valid():
            form = CreatePaymentForm(request.POST)
            obj = form.save(commit=False)
            obj.cash = cash
            obj.user = request.user
            obj.save()
            return redirect('cash-detail', cash.id)
        else:
            form = CreatePaymentForm()
            return redirect('cash-detail', cash.id)

    ctx = {
        'cash': cash,
        'form': form,
    }
    return render(request, 'stock/create_object.html', ctx)


class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = "stock/create_object.html"
    form_class = UpdatePaymentForm
    #success_url = reverse_lazy('cash-detail', kwargs.get('id'))

    def get_success_url(self):
        cash_id = Payment.objects.get(id=self.kwargs['id']).cash_id
        return reverse_lazy('cash-detail', kwargs={'id': cash_id})
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Payment, id=id_)
    
    def form_valid(self, form):
        return super().form_valid(form)


class PaymentDeleteView(DeleteView):
    template_name = 'cash/delete_payment.html'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Payment, id=id_)

    def get_success_url(self):
        return reverse_lazy('cash')


class SearchPaymentView(ListView):
    model = Payment
    template_name = 'stock/search_payment.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PaymentFilter(self.request.GET,
                                          queryset=self.get_queryset())
        return context
    