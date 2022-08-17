from django.http import HttpResponse, FileResponse
from django.views.generic import View
from django.template.loader import get_template

from clever.settings.base import MEDIA_ROOT
from cash.models import Cash
from offer.models import Offer
from production.models import Production, ProductionOrder, ProductionStockIn

from datetime import datetime, timedelta
from io import BytesIO
from xhtml2pdf import pisa

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import landscape, A8



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

        ctx = {
            'cash': cash, 
            'cash_filtered': cash_filtered, 
            'date': date,
            'MEDIA_ROOT': MEDIA_ROOT,
            }
        pdf = html_to_pdf('pdf/cash_report.html', ctx)

        return HttpResponse(pdf, content_type='application/pdf')


class GenerateOrderPdf(View):

    def get(self, request, *args, **kwargs):
        production = ProductionOrder.objects.get(id=self.kwargs['id'])
        ms = production.materialservices_set.all()
        ctx = {
            'production': production,
            'ms': ms, 
            'MEDIA_ROOT': MEDIA_ROOT,
            }
        pdf = html_to_pdf('pdf/order.html', ctx)
       
        return HttpResponse(pdf, content_type='application/pdf')


class GenerateProductionPdf(View):

    def get(self, request, *args, **kwargs):
        production = Production.objects.get(id=self.kwargs['id'])
        pdf = html_to_pdf('pdf/production.html', { 'production': production, 'MEDIA_ROOT': MEDIA_ROOT, } )
        return HttpResponse(pdf, content_type='application/pdf')


def generate_stock_label(request, id):
    stock = ProductionStockIn.objects.get(id=id)
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
    textob.textLine("#{}".format(stock.number)) 
    
    textob.setFont("Helvetica", 14)   
    textob.textLine("{}x{}".format(stock.length, stock.width))
    if stock.rack:
        textob.textLine(f'Regał {stock.rack}')
    textob.textLine(stock.created_by)
    
    

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='#{}.pdf'.format(stock.number))


