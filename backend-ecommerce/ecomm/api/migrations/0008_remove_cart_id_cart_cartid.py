# Generated by Django 4.2.2 on 2023-06-19 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='id',
        ),
        migrations.AddField(
            model_name='cart',
            name='cartid',
            field=models.AutoField(default=2, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]