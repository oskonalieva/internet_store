import re

from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.
from products.models import Product


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = {'products': products}
        return render(request, 'products/product.html', context=data)
