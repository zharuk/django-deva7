# Generated by Django 4.2.6 on 2024-09-12 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0036_rename_user_id_telegramuser_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telegram_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
