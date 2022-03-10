from io import BytesIO

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle

from production.models import ProductionOrder, MaterialServices

from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Frame


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
    x1 = 20
    y1 = 750

    p.drawString(20, 750, "Zamawiający: {}".format(production.customer))
    p.drawString(65, 730, "Adres: {}".format(production.customer.address_line_1))
    p.drawString(109, 710, "{}, {}".format(production.customer.postcode,
                                           production.customer.town_city))
    p.drawString(82, 690, "Tel: {}".format(production.customer.phone_number))
    p.line(0, 672, 1000, 672)
    p.line(0, 670, 1000, 670)

    data = [['Material', 'Usluga', 'Ilosc', 'Cena(m2)', 'Total'],]

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

    p.setTitle(f"Zam_{production}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response
