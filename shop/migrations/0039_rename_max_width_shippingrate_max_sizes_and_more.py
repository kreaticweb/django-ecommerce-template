# Generated by Django 4.2.2 on 2023-06-16 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_shippingrate_max_width_shippingrate_min_width'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingrate',
            old_name='max_width',
            new_name='max_sizes',
        ),
        migrations.RenameField(
            model_name='shippingrate',
            old_name='rate',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='shippingrate',
            name='min_width',
        ),
    ]
