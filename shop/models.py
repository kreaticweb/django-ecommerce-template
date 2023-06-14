from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify
import uuid

from mptt.models import MPTTModel, TreeForeignKey

STATUS_CHOICES = (
    (0, 'Available'),
    (1, 'Coming soon'),
    (2, 'Out of stock'),
    (7, 'Outlet'),
    (3, 'Presale'),
    (4, 'Awaiting stock'),
    (5, 'Hidden'),
    (6, 'Retired'),
)

# TODO: HAcer que no se pueda editar el sku, que si no hay uno introducido se genere y se pueda cambiar solo si se hace un bulk update
def generate_sku(name, category, attribute, variable):
    sku = category + '-' + name + '-' + attribute + '-' + variable
    return sku


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True)
    description = RichTextField(blank=True)

    meta_description = models.TextField(max_length=170, blank=True)
    page_title = models.CharField(max_length=100, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    readonly_fields = ("slug",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Discount(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    date_open = models.DateTimeField(null=True, blank=True)
    date_close = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.ForeignKey('Discount', models.DO_NOTHING, null=True, blank=True)
    description = RichTextField(blank=True)
    meta_description = models.TextField(max_length=170, blank=True)

    category = models.ForeignKey('Category', models.DO_NOTHING, null=True)

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    is_featured = models.BooleanField(default=False)

    in_inventory = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.category:
            self.category = Category.objects.filter(
                name='Uncategorized').get_or_create()
        if not self.sku:
            self.sku = generate_sku(self.name, self.category)
        super().save(*args, **kwargs)
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.DO_NOTHING)
    image = models.FileField(upload_to='img/products/main')


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    values = models.CharField(max_length=255)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True, blank=True)
    image = models.FileField(upload_to='img/products/variant', blank=True)

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    is_featured = models.BooleanField(default=False)
    in_inventory = models.IntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey('Discount', models.DO_NOTHING, null=True, blank=True)


# class Shipment(models.Model):


# class Orders(models.Model):
