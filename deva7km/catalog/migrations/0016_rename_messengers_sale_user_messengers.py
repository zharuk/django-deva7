# Generated by Django 4.2.6 on 2024-02-19 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_sale_messengers_alter_sale_user_telephone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='messengers',
            new_name='user_messengers',
        ),
    ]
