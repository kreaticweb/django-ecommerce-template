from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Category, Product, ProductImage, ProductVariant, ProductAttribute, Discount
from .models import ShippingZone, ShippingMethod, ShippingRate


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
    list_display = ("name", "sku", "price", "discount", "status", "in_inventory")
    filter_horizontal = ('category', "shipping_method")
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
    extra = 1


class ShippingMethodAdmin(admin.ModelAdmin):
    inlines = [ShippingRateInline]
    filter_horizontal = ('zone',)


admin.site.register(ShippingZone)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
