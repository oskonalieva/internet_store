import re

from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.
from products.models import Product, Review, Category


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('categori_id')
        if category_id:
            products = Product.objects.filter(category=Category.objects.get(id=category_id))
        else:
            products = Product.objects.all()

        context = {
            'products': products, }
        return render(request, 'products/product.html', context=context)


def product_detail_view(request, **kwargs):
    if request.method == 'GET':
        product = Product.objects.get(id=kwargs['id'])
        reviews = Review.objects.filter(product_id=kwargs['id'])

        context = {
            'product': product,
            'reviews': reviews
        }
        return render(request, 'products/detail.html', context=context)


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'categories/categories.html', context=context)
