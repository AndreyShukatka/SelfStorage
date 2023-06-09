from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

PRODUCT_GROUP = [
    ('mb', 'Мебель'),
    ('bt', 'Бытовая техника'),
    ('cl', 'Одежда и обувь'),
    ('tl', 'Инструменты'),
    ('ds', 'Посуда'),
    ('bk', 'Книги'),
    ('tr', 'Шины'),
    ('vb', 'Велосипеды'),
    ('bs', 'Мотоциклы и скутеры'),
    ('st', 'Спортивный инвентарь')
]

DELIVERY_TERMS = [
    ('sm', 'Самовывоз'),
    ('dt', 'Доставка')
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Missing email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя', max_length=250, default='some_user', blank=True)
    email = models.EmailField('Адрес электронной почты', max_length=50, unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_staff = models.BooleanField('Является сотрудником', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.username


class Cargo(models.Model):
    title = models.CharField('Наименование', max_length=30, blank=True)
    group = models.CharField('Группа груза', max_length=6, choices=PRODUCT_GROUP)
    weight = models.IntegerField('Вес, кг', blank=True, null=True)
    length = models.IntegerField('Длина, см', blank=True, null=True)
    width = models.IntegerField('Ширина, см', blank=True, null=True)
    height = models.IntegerField('Высота, см', blank=True, null=True)
    photo = models.ImageField('Фото груза', upload_to='media/', blank=True, null=True)

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'


class StorageAddress(models.Model):
    address = models.CharField(max_length=150, verbose_name='Адрес')
    occupied = models.IntegerField(default=0, verbose_name='Занято боксов')

    class Meta:
        verbose_name = 'Адрес склада'
        verbose_name_plural = 'Адреса складов'

    def __str__(self) -> str:
        return self.address

    def get_storage_quantity(self):
        return self.storages.all().count()


class Storage(models.Model):
    title = models.CharField('Наименование', max_length=100, blank=True)
    length = models.IntegerField('Длина, м')
    width = models.IntegerField('Ширина, м')
    height = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Высота, м')
    photo = models.ImageField('Фото контейнера', blank=True, null=True)
    temperature = models.IntegerField(verbose_name='Температура в боксе')
    address = models.ForeignKey(StorageAddress, on_delete=models.CASCADE, related_name='storages', verbose_name='Адрес')
    price = models.IntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Контейнер'
        verbose_name_plural = 'Контейнеры'

    def __str__(self) -> str:
        return f'{self.length} - {self.width} - {self.height} м'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Клиент',
        related_name='Заказы',
        on_delete=models.CASCADE
    )
    storage = models.ForeignKey(
        Storage,
        verbose_name='Контейнер',
        related_name='Контейнеры',
        on_delete=models.PROTECT)
    reception_conditions = models.CharField(
        'Условия принятия груза от клиента',
        max_length=2,
        choices=DELIVERY_TERMS)
    delivery_conditions = models.CharField(
        'Условия доставки груза клиенту',
        max_length=2,
        choices=DELIVERY_TERMS)
    reception_date = models.DateField('Дата принятия груза', blank=True, null=True)
    delivery_date = models.DateField('Дата возврата груза', blank=True, null=True)
    paid_to = models.DateField('Оплачено до')
    comment = models.CharField('Комментарий к заказу', max_length=100, blank=True, null=True)
    qr_code = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class PaymentOrder(models.Model):
    """Модель сущности Оплата"""
    PENDING = 'PND'
    SUCCESS = 'SCS'
    CANCELED = 'CNC'

    PAYMENT_STATUS_CHOICE = [
        (PENDING, 'Ожидает подтверждения'),
        (SUCCESS, 'Оплачен'),
        (CANCELED, 'Отменен')
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Заказ',
        default=None,
        blank=True,
        null=True
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='storage_payments',
        verbose_name='Хранилище'
    )
    card_number = models.CharField(
        max_length=50,
        verbose_name='Последние 4 цифры номера карты'
    )
    payment_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='ID платежа'
    )
    status = models.CharField(
        max_length=3,
        choices=PAYMENT_STATUS_CHOICE,
        default=PENDING,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
