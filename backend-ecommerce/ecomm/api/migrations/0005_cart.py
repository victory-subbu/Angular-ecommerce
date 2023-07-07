# Generated by Django 4.2.2 on 2023-06-18 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_color', models.CharField(max_length=100)),
                ('product_category', models.CharField(max_length=100)),
                ('product_description', models.TextField()),
                ('product_image', models.FileField(blank=True, null=True, upload_to='product_images')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.customersignup')),
            ],
        ),
    ]