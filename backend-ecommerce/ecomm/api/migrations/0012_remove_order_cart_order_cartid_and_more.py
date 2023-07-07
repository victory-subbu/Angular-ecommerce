# Generated by Django 4.2.2 on 2023-06-19 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_order_cart_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cartid',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product_category',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product_color',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product_description',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product_image',
            field=models.FileField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10),
            preserve_default=False,
        ),
    ]