# Generated by Django 4.2.2 on 2023-06-14 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_product_discount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Discounts',
            new_name='Discount',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shop.discount'),
        ),
    ]
