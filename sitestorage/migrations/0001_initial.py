# Generated by Django 4.2 on 2023-04-20 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sitestorage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(default='some_user', max_length=250, verbose_name='Имя')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Адрес электронной почты')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Является сотрудником')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
            managers=[
                ('objects', sitestorage.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True, verbose_name='Наименование')),
                ('group', models.CharField(choices=[('mb', 'Мебель'), ('bt', 'Бытовая техника'), ('cl', 'Одежда и обувь'), ('tl', 'Инструменты'), ('ds', 'Посуда'), ('bk', 'Книги'), ('tr', 'Шины'), ('vb', 'Велосипеды'), ('bs', 'Мотоциклы и скутеры'), ('st', 'Спортивный инвентарь')], max_length=6, verbose_name='Группа груза')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='Вес, кг')),
                ('length', models.IntegerField(blank=True, null=True, verbose_name='Длина, см')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='Ширина, см')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='Высота, см')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Фото груза')),
            ],
            options={
                'verbose_name': 'Груз',
                'verbose_name_plural': 'Грузы',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=10, null=True, verbose_name='Наименование')),
                ('length', models.IntegerField(verbose_name='Длина, м')),
                ('width', models.IntegerField(verbose_name='Ширина, м')),
                ('height', models.IntegerField(verbose_name='Высота, м')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Фото контейнера')),
            ],
            options={
                'verbose_name': 'Контейнер',
                'verbose_name_plural': 'Контейнеры',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reception_conditions', models.CharField(choices=[('sm', 'Самовывоз'), ('dt', 'Доставка')], max_length=2, verbose_name='Условия принятия груза от клиента')),
                ('delivery_conditions', models.CharField(choices=[('sm', 'Самовывоз'), ('dt', 'Доставка')], max_length=2, verbose_name='Условия доставки груза клиенту')),
                ('reception_date', models.DateField(blank=True, null=True, verbose_name='Дата принятия груза')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Дата возврата груза')),
                ('paid_to', models.DateField(verbose_name='Оплачено до')),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий к заказу')),
                ('qr_code', models.CharField(blank=True, max_length=40, null=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Грузы', to='sitestorage.cargo', verbose_name='Груз')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Контейнеры', to='sitestorage.storage', verbose_name='Контейнер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Заказы', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
