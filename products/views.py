import re

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from products.models import Product, Review, Category
from products.forms import ProductCreateForm, ReviewCreateForm


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
    form = ReviewCreateForm(data=request.POST)
    product = Product.objects.get(id=kwargs['id'])
    if request.method == 'GET':
        reviews = Review.objects.filter(product_id=kwargs['id'])
        context = {
            'product': product,
            'reviews': reviews,
            'form': ReviewCreateForm
        }
        return render(request, 'products/detail.html', context=context)

    elif request.method == 'POST':
        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product=product)
            return redirect(f'/products/{kwargs["id"]}/')


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'categories/categories.html', context=context)


def create_products_view(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            Product.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate', 5),
                price=form.cleaned_data.get('price'))

            return redirect('/products/')





