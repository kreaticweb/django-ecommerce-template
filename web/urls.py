from django.urls import path, re_path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.products, name='products'),
    path('productos/<str:category_slug>', views.category, name='category'),
    path('productos/<str:category_slug>/<str:product_slug>', views.product, name='product')
]
