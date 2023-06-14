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
    list_display = ("sku", "name", "category")
    list_display_links = ("name",)
    inlines = [ProductAttributeInline, ProductVariantInline, ProductImageAdmin]
    readonly_fields = ("slug", "num_visits", "last_visit")


admin.site.register(Discount)
