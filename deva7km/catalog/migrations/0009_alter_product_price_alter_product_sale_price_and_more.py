# Generated by Django 4.2.6 on 2023-12-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_productmodification_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(default=0, verbose_name='Цена распродажи'),
        ),
        migrations.AlterField(
            model_name='productmodification',
            name='sale_price',
            field=models.IntegerField(default=0, verbose_name='Цена распродажи'),
        ),
    ]
