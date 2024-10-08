# Generated by Django 4.2.6 on 2024-09-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0040_remove_preorder_is_bulk_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='preorder',
            name='message_status',
            field=models.CharField(choices=[('none', 'Не отправлено'), ('ready', 'Сообщение о готовности отправлено'), ('shipped', 'Сообщение об отправке отправлено')], default='none', max_length=10, verbose_name='Статус отправки сообщений'),
        ),
    ]
