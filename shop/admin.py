from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Category, Product, ProductImage, ProductVariant, ProductAttribute, Discount


# Register your models here.
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    readonly_fields = ("slug",)


admin.site.register(Category, CustomMPTTModelAdmin)


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


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'products_linked']
    readonly_fields = ['products_linked']

    def products_linked(self, obj):
        return ", ".join([str(product) for product in obj.product_set.all()])


admin.site.register(Discount, DiscountAdmin)
