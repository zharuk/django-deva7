# Generated by Django 4.2.6 on 2024-06-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_alter_preorder_drop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preorder',
            name='drop',
            field=models.BooleanField(default=False, verbose_name='Дроп'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Имя и Фамилия'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='receipt_issued',
            field=models.BooleanField(default=False, verbose_name='Чек'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='shipped_to_customer',
            field=models.BooleanField(default=False, verbose_name='Отправлен'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='text',
            field=models.TextField(blank=True, verbose_name='Инфо'),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='ttn',
            field=models.CharField(blank=True, max_length=30, verbose_name='ТТН'),
        ),
    ]