# Generated by Django 4.2.6 on 2023-12-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_remove_product_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodification',
            name='sale_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Цена распродажи'),
        ),
    ]