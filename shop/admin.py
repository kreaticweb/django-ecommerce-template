from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Category, Product, ProductImage, ProductVariant, ProductAttribute, Discount
from .models import Shipping, ShippingMethod, ShippingRate


# Register your models here.
@admin.register(Category)
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    readonly_fields = ("slug",)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "discount", "status", "in_inventory")
    list_display_links = ("name",)
    inlines = [ProductAttributeInline, ProductVariantInline, ProductImageAdmin]
    readonly_fields = ("slug", "num_visits", "last_visit")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'products_linked']
    readonly_fields = ['products_linked']

    def products_linked(self, obj):
        return ", ".join([str(product) for product in obj.product_set.all()])



class ShippingMethodInline(admin.TabularInline):
    model = ShippingMethod

class ShippingRateInline(admin.TabularInline):
    model = ShippingRate

class ShippingAdmin(admin.ModelAdmin):
    inlines = [ShippingMethodInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = super().get_inline_instances(request, obj)
        inlines.append(ShippingMethodInline)
        return inlines

class ShippingMethodAdmin(admin.ModelAdmin):
    inlines = [ShippingRateInline]

admin.site.register(Shipping, ShippingAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(ShippingRate)