# Generated by Django 4.2.2 on 2023-06-13 16:11

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productimage',
            field=models.FileField(blank=True, null=True, upload_to=register.models.product_images),
        ),
    ]