import re

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from products.models import Product, Review, Category
from products.forms import ProductCreateForm, ReviewCreateForm

PAGINATION_LIMIT = 3

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
            search = request.GET.get('search')
            page = request.GET.get('page', 1)
            if search is not None:
                products = Product.objects.filter(category__name__icontains=search) or \
                           Product.objects.filter(description__icontains=search)
            max_page = products.__len__() / PAGINATION_LIMIT
            if round(max_page) < max_page:
                max_page = int(max_page) + 1
            products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]

            context = {
                'products': products,
                'max_page':(1, max_page+1)
            }

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





