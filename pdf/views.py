from io import BytesIO

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle

from cash.models import Cash
from production.models import ProductionOrder

from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame

from django.views.generic import View
from .process import html_to_pdf 
from django.template.loader import render_to_string


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        cashes = Cash.objects.all()
        date = datetime.now()
        open('templates/temp.html', "w").write(render_to_string('pdf/cash_report.html', {'cashes': cashes, 'date': date,}))
        
        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf, content_type='application/pdf')


def generate_pdf(request, id):

    production = ProductionOrder.objects.get(id=id)
    ms = production.materialservices_set.all()
    d = datetime.today()

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'inline: filename="{production}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Verdana", 12, leading=None)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(195, 805, "Zamówienie nr {} ".format(production))
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    p.drawString(20, 750, "Zamawiający: {}".format(production.customer))
    p.drawString(65, 730, "Adres: {}".format(production.customer.address_line_1))
    p.drawString(109, 710, "{}, {}".format(production.customer.postcode,
                                           production.customer.town_city))
    p.drawString(82, 690, "Tel: {}".format(production.customer.phone_number))
    p.line(0, 672, 1000, 672)
    p.line(0, 670, 1000, 670)

    data = [['Material', 'Usluga', 'Ilosc', 'Cena(m2)', 'Suma'],]

    for i in production.materialservices_set.all():
        print(i.material)
        data += [[i.material,
                  i.services,
                  "{}m2".format(i.area),
                  "{}pln".format(i.price),
                  "{0:.2f}pln".format(i.total())]]

    data.append(['', '', '', 'Razem', '{0:.2f}pln'.format(production.get_total())])
    GRID_STYLE = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('ALIGN', (1, 1), (-1, -1), 'LEFT')]
            )

    t = Table(data, None, None)
    t.setStyle(GRID_STYLE)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    story = []
    story.append(t)
    f = Frame(0, -2.8*inch, 8.3*inch, 11.7*inch)
    f.addFromList(story, p)

    footer_style = styles['Normal']
    footer_style.alignment = 1 
    footer = Paragraph("Dokument wygenerowany automatycznie przez system Nesting Polska sp. z.o.o ", footer_style)

    story.append(Paragraph("Data wystawienia: {}".format(d.strftime('%d-%m-%Y')), footer_style))
    
    f2 = Frame(0, 0, 8.3*inch, 1*inch, showBoundary=1)
    f2.addFromList(story, p)

    p.setTitle(f"Zam_{production}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


def cash_raport(request, id):
    cash = Cash.objects.get(id=id)
    payments = cash.payment_set.all()
    
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'inline: filename="{cash}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Verdana", 12, leading=None)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(195, 805, "Raport nr {} ".format(cash))
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    p.line(0, 672, 1000, 672)
    p.line(0, 670, 1000, 670)

    data = [['Material', 'Usluga', 'Ilosc', 'Cena(m2)', 'Suma'],]

    for i in payments:
        print(i.material)
        data += [[i.material,
                  i.services,
                  "{}m2".format(i.area),
                  "{}pln".format(i.price),
                  "{0:.2f}pln".format(i.total())]]

    GRID_STYLE = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('ALIGN', (1, 1), (-1, -1), 'LEFT')]
            )

    t = Table(data, None, None)
    t.setStyle(GRID_STYLE)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    story = []
    story.append(t)
    f = Frame(0, -2.8*inch, 8.3*inch, 11.7*inch)
    f.addFromList(story, p)

    footer_style = styles['Normal']
    footer_style.alignment = 1 
    footer = Paragraph("Dokument wygenerowany automatycznie przez system Nesting Polska sp. z.o.o ", footer_style)

    # story.append(Paragraph("Data wystawienia: {}".format(d.strftime('%d-%m-%Y')), footer_style))
    
    f2 = Frame(0, 0, 8.3*inch, 1*inch, showBoundary=1)
    f2.addFromList(story, p)

    p.setTitle(f"Raport_{cash}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


