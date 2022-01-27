from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Stock


@staff_member_required
def stock(request):
	
	stock = Stock.objects.all()
	

	for i in stock:
		print(i.material)


	context = {
		'stock': stock,
	}
	return render(request, 'stock/home.html', context)