# Generated by Django 4.2.6 on 2024-03-03 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_product_retail_price_product_retail_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='delivery_locality',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='delivery_post_office',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='delivery_service',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='prepayment',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user_email',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user_messengers',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user_surname',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='user_telephone',
        ),
    ]