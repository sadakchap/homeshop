from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.

def product_list(request, cat_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=category)
    context = {
        'products': products,
        'category': category,
        'categories': categories
    }
    return render(request, 'home.html', context=context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", {'product':product})