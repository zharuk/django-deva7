# Generated by Django 4.2.6 on 2024-09-15 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0037_telegramuser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.BigIntegerField(unique=True, verbose_name='Идентификатор пользователя telegram'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telegram_user', to=settings.AUTH_USER_MODEL, verbose_name='Связь с User'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя пользователя @ telegram'),
        ),
    ]