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


categories = Category.objects.filter(is_featured=False)
featured_categories = Category.objects.filter(is_featured=True)


def products(request):
    context = {
        "categories": categories,
        "featured_categories": featured_categories,

        "page_title": "Tienda",
    }
    return render(request, 'shop.html', context)


def category(request, category_slug):
    current_category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=current_category)
    context = {
        "categories": categories,
        "featured_categories": featured_categories,

        "current_category": current_category,
        "products": products
    }
    return render(request, 'shop.html', context)

