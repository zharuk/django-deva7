# Generated by Django 4.2.6 on 2024-03-03 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_rename_messengers_sale_user_messengers'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='retail_price',
            field=models.IntegerField(default=0, verbose_name='Цена в розницу'),
        ),
        migrations.AddField(
            model_name='product',
            name='retail_sale_price',
            field=models.IntegerField(default=0, verbose_name='Цена распродажи в розницу'),
        ),
    ]
