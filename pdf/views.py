# -*- coding: latin-1 -*-
from django.http import HttpResponse


from cash.models import Cash
from offer.models import Offer


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

    pass


# def generate_pdf(request, id):

#     production = ProductionOrder.objects.get(id=id)
#     ms = production.materialservices_set.all()
#     d = datetime.today()

#     pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

#     response = HttpResponse(content_type='application/pdf')

#     response['Content-Disposition'] = f'inline: filename="{production}.pdf"'

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)

#     p.setFont("Verdana", 12, leading=None)
#     p.setFillColorRGB(0, 0, 0)
#     p.drawString(195, 805, "Zamówienie nr {} ".format(production))
#     p.line(0, 780, 1000, 780)
#     p.line(0, 778, 1000, 778)
#     p.drawString(20, 750, "Zamawiający: {}".format(production.customer))
#     p.drawString(65, 730, "Adres: {}".format(production.customer.address_line_1))
#     p.drawString(109, 710, "{}, {}".format(production.customer.postcode,
#                                            production.customer.town_city))
#     p.drawString(82, 690, "Tel: {}".format(production.customer.phone_number))
#     p.line(0, 672, 1000, 672)
#     p.line(0, 670, 1000, 670)

#     data = [['Material', 'Usluga', 'Ilosc', 'Cena(m2)', 'Suma'],]

#     for i in production.materialservices_set.all():
#         print(i.material)
#         data += [[i.material,
#                   i.services,
#                   "{}m2".format(i.area),
#                   "{}pln".format(i.price),
#                   "{0:.2f}pln".format(i.total())]]

#     data.append(['', '', '', 'Razem', '{0:.2f}pln'.format(production.get_total())])
#     GRID_STYLE = TableStyle(
#             [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#              ('ALIGN', (1, 1), (-1, -1), 'LEFT')]
#             )

#     t = Table(data, None, None)
#     t.setStyle(GRID_STYLE)

#     styles = getSampleStyleSheet()
#     styleN = styles['Normal']

#     story = []
#     story.append(t)
#     f = Frame(0, -2.8*inch, 8.3*inch, 11.7*inch)
#     f.addFromList(story, p)

#     footer_style = styles['Normal']
#     footer_style.alignment = 1 
#     footer = Paragraph("Dokument wygenerowany automatycznie przez system Nesting Polska sp. z.o.o ", footer_style)

#     story.append(Paragraph("Data wystawienia: {}".format(d.strftime('%d-%m-%Y')), footer_style))
    
#     f2 = Frame(0, 0, 8.3*inch, 1*inch, showBoundary=1)
#     f2.addFromList(story, p)

#     p.setTitle(f"Zam_{production}")
#     p.showPage()
#     p.save()

#     pdf = buffer.getvalue()
#     buffer.close()

#     response.write(pdf)
#     return response
