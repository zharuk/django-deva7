# Generated by Django 4.2.6 on 2024-09-17 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0041_preorder_message_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preorder',
            name='message_status',
        ),
        migrations.AddField(
            model_name='preorder',
            name='ready_for_shipment',
            field=models.BooleanField(default=False, verbose_name='Готов к отправке'),
        ),
        migrations.AddField(
            model_name='preorder',
            name='shipped',
            field=models.BooleanField(default=False, verbose_name='Отправлен'),
        ),
    ]
