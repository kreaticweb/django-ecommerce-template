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


class ShippingZone(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    zone = models.ManyToManyField(ShippingZone)
    info = RichTextField(blank=True)

    def __str__(self):
        zone_names = ', '.join(str(zone) for zone in self.zone.all())
        return f"{zone_names}, {self.name}"


class ShippingRate(models.Model):
    method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    max_width = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    min_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.method.name}: {self.min_weight}-{self.max_weight} - ${self.price}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.ForeignKey('Discount', models.DO_NOTHING, null=True, blank=True)
    description = RichTextField(blank=True)
    meta_description = models.TextField(max_length=170, blank=True)

    category = models.ManyToManyField('Category')

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    is_featured = models.BooleanField(default=False)

    in_inventory = models.IntegerField(default=1)
    shipping_method = models.ManyToManyField(ShippingMethod)
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
    sku = models.CharField(max_length=20, unique=True)
    image = models.FileField(upload_to='img/products/variant', blank=True)

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    is_featured = models.BooleanField(default=False)
    in_inventory = models.IntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey('Discount', models.DO_NOTHING, null=True, blank=True)

# class Orders(models.Model):
