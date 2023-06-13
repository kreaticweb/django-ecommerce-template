from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Category, Product


# Register your models here.
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    readonly_fields = ("slug",)


admin.site.register(Category, CustomMPTTModelAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category")
    list_display_links = ("name",)
    readonly_fields = ("slug", "num_visits")




