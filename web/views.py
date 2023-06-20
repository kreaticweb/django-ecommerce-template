from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from shop.models import Category, Product


# Create your views here.
def index(request):
    context = {

    }
    if 'contact_form' in request.POST:
        return HttpResponseRedirect('/gracias/')
    else:
        return render(request, 'index.html', context)


def products(request):
    categories = Category.objects.all()

    context = {
        "ShopTitle": "Tienda",
        "categories": categories,
    }
    return render(request, 'shop.html', context)


def category(request, *args, **kwargs):
    categories = Category.objects.all()
    if kwargs.get('subcategory_slug'):
        category_slug = kwargs.get('subcategory_slug')
    else:
        category_slug = kwargs.get('category_slug')

    current_category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=current_category)
    context = {
        "ShopTitle": current_category,
        "categories": categories,

        "category": current_category,
        "products": products
    }
    return render(request, 'shop.html', context)

