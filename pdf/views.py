# -*- coding: latin-1 -*-
from django.http import HttpResponse


from cash.models import Cash
from offer.models import Offer
from production.models import ProductionOrder


from datetime import datetime, timedelta

from django.views.generic import View

from django.template.loader import render_to_string




from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa  

from clever.settings.base import  MEDIA_ROOT

def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode('utf8')), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

class GeneratePdfOffer(View):
    def get(self, request, *args, **kwargs):
        offer = Offer.objects.get(id=self.kwargs['id'])

        ctx = {'offer': offer, 'MEDIA_ROOT': MEDIA_ROOT}
        pdf = html_to_pdf('pdf/offer.html', ctx)
       
        return HttpResponse(pdf, content_type='application/pdf')

class GenereatePdfRaport(View):
    def get(self, request, *args, **kwargs):  

        cash = Cash.objects.get(id=self.kwargs['id'])
        today = datetime.today()

        if self.kwargs['date'] == 'month':
            last_month = today - timedelta(days=31)
            cash_filtered = cash.payment_set.filter(date__gte=last_month)
            date = 'month'

        if self.kwargs['date'] == 'week':
            last_week = today - timedelta(days=7)
            cash_filtered = cash.payment_set.filter(date__week=last_week.isocalendar().week)
            date = 'week'
        
        if self.kwargs['date'] == 'today':
            cash_filtered = cash.payment_set.filter(date__date=today)
            date = 'today'

        
        ctx = {'cash': cash, 
          'cash_filtered': cash_filtered, 
          'date': date,
          'MEDIA_ROOT': MEDIA_ROOT,}
        pdf = html_to_pdf('pdf/cash_report.html', ctx)

        return HttpResponse(pdf, content_type='application/pdf')


class GenerateOrderPdf(View):

    def get(self, request, *args, **kwargs):
        production = ProductionOrder.objects.get(id=self.kwargs['id'])
        ms = production.materialservices_set.all()
        #d = datetime.today()

        ctx = {'production': production, 'ms': ms, 'MEDIA_ROOT': MEDIA_ROOT}
        pdf = html_to_pdf('pdf/order.html', ctx)
       
        return HttpResponse(pdf, content_type='application/pdf')

