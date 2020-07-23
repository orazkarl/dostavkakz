from django.db import models
from user_auth.models import User
import numpy as np

slug_help_text = "Слаг - это короткая метка для представления страницы в URL. \
Содержит только буквы, цифры, подчеркивания или дефисы."

class Category(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class FoodTag(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Тег еды'
        verbose_name_plural = 'Тег еды'

    def __str__(self):
        return self.name


class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)
    description = models.CharField('Описание', max_length=500, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='store/')
    # category = models.ForeignKey(FoodCategory, verbose_name='Тэг', null=True, blank=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(FoodTag, related_name='tags', null=True, blank=True)
    time_open = models.TimeField('Открывается', null=True, blank=True)
    time_closed = models.TimeField('Закрывается', null=True, blank=True)
    latitude = models.CharField('Широота', max_length=50, null=True, blank=True)
    longitude = models.CharField('Высота', max_length=50, null=True, blank=True)
    avg_check = models.PositiveIntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведении'

    def __str__(self):
        return self.name

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        avg_rating = np.mean(list(all_ratings))
        if str(avg_rating) == 'nan':
            return 0
        return round(avg_rating)

    def average_check(self):
        all_prices = map(lambda x: x.price, self.product_set.all())
        avg_check = np.mean(list(all_prices))
        if str(avg_check) == 'nan':
            self.avg_check = 0
            return 0
        avg_check = int(avg_check)
        if avg_check <= 1500:
            self.avg_check = 1
            self.save()
            return 1
        elif avg_check > 1500 and avg_check <= 4000:
            self.avg_check = 2
            self.save()
            return 2
        elif avg_check > 4000 and avg_check <= 8000:
            self.avg_check = 3
            self.save()
            return 3
        else:
            self.avg_check = 4
            self.save()
            return 4


class Product(models.Model):
    id_code = models.CharField('КОД', max_length=100, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, verbose_name='Заведение')
    category = models.ForeignKey(FoodTag, on_delete=models.DO_NOTHING, verbose_name='Тег', null=True, blank=True)
    name = models.CharField('Название', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    description = models.CharField('Описание', max_length=100, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d', default='store/KFC_logo.png')
    quantity = models.PositiveIntegerField('Количество', null=True, blank=True)
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Заведения')
    pub_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField('Комментарий', max_length=250, null=True, blank=True)
    rating = models.PositiveIntegerField('Рейтинг', choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.store}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    store_item = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Заведения')
    added_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.store_item}"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('1', 'Не оплачен'),
        ('2', 'Оплачен'),
        ('3', 'Доставлен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    order_item = models.CharField('Заказ', max_length=1000, null=True, blank=True)
    address = models.CharField('Адрес', null=True, blank=True, max_length=250)
    total_price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    status = models.CharField('Статус', choices=ORDER_STATUS_CHOICES, max_length=25, null=True, blank=True)
    comment = models.CharField('Комментарии', max_length=250, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.order_item
