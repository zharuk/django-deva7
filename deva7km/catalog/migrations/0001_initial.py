# Generated by Django 4.2.6 on 2023-12-03 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование категории')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Слаг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товара',
                'ordering': ('name',),
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата оприходования')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('completed', 'Завершено'), ('canceled', 'Отменено')], default='completed', max_length=20, verbose_name='Статус')),
                ('source', models.CharField(choices=[('site', 'Сайт'), ('telegram', 'telegram')], default='site', max_length=20, verbose_name='Источник продажи')),
            ],
            options={
                'verbose_name': 'Оприходование',
                'verbose_name_plural': 'Оприходования',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('sku', models.CharField(max_length=50, unique=True, verbose_name='Артикул')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Цена')),
                ('sale_price', models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Цена распродажи')),
                ('old_price', models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=4, verbose_name='Старая цена')),
                ('currency', models.CharField(choices=[('UAH', 'Гривны (грн)'), ('USD', 'Доллары (USD)'), ('EUR', 'Евро (EUR)')], default='UAH', max_length=3, verbose_name='Валюта')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Слаг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_sale', models.BooleanField(default=False, verbose_name='Распродажа')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включен')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
                ('colors', models.ManyToManyField(blank=True, to='catalog.color', verbose_name='Цвета')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ProductModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Остаток')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('currency', models.CharField(choices=[('UAH', 'Гривны (грн)'), ('USD', 'Доллары (USD)'), ('EUR', 'Евро (EUR)')], default='UAH', max_length=3, verbose_name='Валюта')),
                ('custom_sku', models.CharField(blank=True, max_length=50, verbose_name='Артикул комплектации')),
                ('slug', models.SlugField(blank=True, max_length=200, verbose_name='Слаг модификации')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включен')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.color', verbose_name='Цвет')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modifications', to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Модификация товара',
                'verbose_name_plural': 'Модификации товаров',
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата возврата')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('source', models.CharField(choices=[('site', 'Сайт'), ('telegram', 'telegram')], default='site', max_length=20, verbose_name='Источник продажи')),
            ],
            options={
                'verbose_name': 'Возврат',
                'verbose_name_plural': 'Возвраты',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата продажи')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('completed', 'Завершено'), ('canceled', 'Отменено')], default='completed', max_length=20, verbose_name='Статус')),
                ('payment_method', models.CharField(choices=[('cash', 'Наличная оплата'), ('non_cash', 'Безналичная оплата')], default='cash', max_length=20, verbose_name='Способ оплаты')),
                ('source', models.CharField(choices=[('site', 'Сайт'), ('telegram', 'telegram')], default='site', max_length=20, verbose_name='Источник продажи')),
            ],
            options={
                'verbose_name': 'Продажа',
                'verbose_name_plural': 'Продажи',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='Идентификатор пользователя')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя пользователя')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия')),
                ('is_bot', models.BooleanField(default=False, verbose_name='Бот')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('role', models.CharField(choices=[('admin', 'Админ'), ('seller', 'Продавец'), ('unauthorized', 'Неавторизованный')], default='unauthorized', max_length=12, verbose_name='Роль')),
            ],
            options={
                'verbose_name': 'Пользователь Telegram',
                'verbose_name_plural': 'Пользователи Telegram',
            },
        ),
        migrations.CreateModel(
            name='WriteOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата списания')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('completed', 'Завершено'), ('canceled', 'Отменено')], default='completed', max_length=20, verbose_name='Статус')),
                ('source', models.CharField(choices=[('site', 'Сайт'), ('telegram', 'telegram')], default='site', max_length=20, verbose_name='Источник продажи')),
                ('telegram_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.telegramuser', verbose_name='Пользователь Telegram')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Списание товара',
                'verbose_name_plural': 'Списания товара',
            },
        ),
        migrations.CreateModel(
            name='WriteOffItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество списываемого')),
                ('product_modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productmodification', verbose_name='Модификация товара')),
                ('write_off', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.writeoff', verbose_name='Списание товара')),
            ],
            options={
                'verbose_name': 'Элемент списания товара',
                'verbose_name_plural': 'Элементы списания товара',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество продаваемого')),
                ('product_modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productmodification', verbose_name='Модификация товара')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.sale', verbose_name='Продажа')),
            ],
            options={
                'verbose_name': 'Элемент продажи',
                'verbose_name_plural': 'Элементы продажи',
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='telegram_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.telegramuser', verbose_name='Пользователь Telegram'),
        ),
        migrations.AddField(
            model_name='sale',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='ReturnItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество возвращаемого')),
                ('product_modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productmodification', verbose_name='Модификация товара')),
                ('return_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.return', verbose_name='Возврат')),
            ],
            options={
                'verbose_name': 'Элемент возврата',
                'verbose_name_plural': 'Элементы возврата',
            },
        ),
        migrations.AddField(
            model_name='return',
            name='telegram_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.telegramuser', verbose_name='Пользователь Telegram'),
        ),
        migrations.AddField(
            model_name='return',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='productmodification',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.size', verbose_name='Размер'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='catalog.size', verbose_name='Размеры'),
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество оприходуемого')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.inventory', verbose_name='Оприходование')),
                ('product_modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productmodification', verbose_name='Модификация товара')),
            ],
            options={
                'verbose_name': 'Элемент оприходования',
                'verbose_name_plural': 'Элементы оприходования',
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='telegram_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.telegramuser', verbose_name='Пользователь Telegram'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Оригинальное изображение')),
                ('modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.productmodification', verbose_name='Модификация товара')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товара',
            },
        ),
        migrations.AlterUniqueTogether(
            name='productmodification',
            unique_together={('product', 'color', 'size')},
        ),
    ]