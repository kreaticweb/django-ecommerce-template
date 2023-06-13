from ckeditor.fields import RichTextField
from django.db import models
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey


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


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, blank=True)
    description = RichTextField(blank=True)
    meta_description = models.TextField(max_length=170, blank=True)

    category = models.ForeignKey('Category', models.DO_NOTHING, null=True)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.DO_NOTHING)
    images = models.FileField(upload_to='img/products/secondary')
