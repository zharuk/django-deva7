# Generated by Django 4.2.6 on 2024-09-17 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0042_remove_preorder_message_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preorder',
            name='ready_for_shipment',
        ),
        migrations.RemoveField(
            model_name='preorder',
            name='shipped',
        ),
    ]