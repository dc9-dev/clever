from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from production.models import ProductionOrder

from datetime import datetime


def generate_pdf(request):

    production = ProductionOrder.objects.get(id=1)
    ms = production.materialservices_set.all()
    d = datetime.today()

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'inline: filename="{d}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Verdana", 12, leading=None)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(195, 800, "Zamówienie nr {} ".format(production))
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750

    p.drawString(20, 750, "Zamawiający: {}".format(production.customer))
    p.drawString(65, 730, "Adres: {}".format(production.customer.address_line_1))
    p.drawString(109, 710, "{}, {}".format(production.customer.postcode,
                                           production.customer.town_city))
    p.drawString(83, 690, "Tel: {}".format(production.customer.phone_number))
    # for i in Production.objects.all():
    #     p.setFont("Helvetica", 15, leading=None)
    #     p.drawString(x1, y1-12, f"{i}")

    p.setTitle(f"report on {d}")
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response