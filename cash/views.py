from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy 
from django.http.response import JsonResponse
from .forms import CreatePaymentForm, UpdatePaymentForm
from .filters import PaymentFilter
from .models import Payment, Cash


class PaymentsListView(ListView):
    model = Payment
    template_name = 'cash/home_payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashes'] = Cash.objects.all()
        return context

# class PaymentDetailView(DetailView):
#     model = Payment
#     template_name = ""

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = "stock/create_object.html"
    form_class = CreatePaymentForm
    success_url = reverse_lazy('cash')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = "stock/create_object.html"
    form_class = UpdatePaymentForm
    success_url = reverse_lazy('cash')
    
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
    