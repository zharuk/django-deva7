# Generated by Django 4.2.6 on 2024-09-17 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0043_remove_preorder_ready_for_shipment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='preorder',
            name='ready_for_shipment_notified',
            field=models.BooleanField(default=False, verbose_name='Уведомление о готовности к отправке отправлено'),
        ),
        migrations.AddField(
            model_name='preorder',
            name='shipped_notified',
            field=models.BooleanField(default=False, verbose_name='Уведомление об отправке отправлено'),
        ),
    ]
