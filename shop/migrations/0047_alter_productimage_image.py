# Generated by Django 4.2.2 on 2023-06-23 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0046_alter_product_shipping_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.FileField(upload_to='static/img/products/'),
        ),
    ]
