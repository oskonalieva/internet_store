from django.shortcuts import render, redirect
# Create your views here.
from products.models import Product, Review, Category
from products.forms import ProductCreateForm, ReviewCreateForm
from django.views.generic import ListView, CreateView, DetailView

PAGINATION_LIMIT = 3





class MainView(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductsView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        category_id = self.request.GET.get('categori_id')
        search = self.request.GET.get('search')
        page = self.request.GET.get('page', 1)

        if category_id:
            products = Product.objects.filter(category=Category.objects.get(id=category_id))
        else:
            products = Product.objects.all()
        if search:
            products = Product.objects.filter(title__icontains=search)
        else:
            max_page = products.__len__() / PAGINATION_LIMIT
            max_page = int(max_page) + 1
            products = products[PAGINATION_LIMIT * (int(page) - 1): PAGINATION_LIMIT * int(page)]
        return {
            'products': products,
            'max_page': list(range(1, max_page + 1))
        }


class ProductDetail(DetailView,CreateView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        reviews = Review.objects.filter(product_id=self.get_object())
        return {
            'product': self.get_object(),
            'reviews': reviews,
            'form': ReviewCreateForm
        }
    def post(self, request, *args, **kwargs):
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product=self.get_object())

            return redirect(f'/products/{kwargs["id"]}/')


class CategoriesView(ListView):
    queryset = Category.objects.all()
    template_name = 'categories/categories.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        return {'categories': self.queryset}


class ProductCreate(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm
    def get_context_data(self, *, object_list=None, **kwargs):
            return {
            'form': ProductCreateForm
                    }
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            Product.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate', 5),
                price=form.cleaned_data.get('price'))
            return redirect('/products/')
