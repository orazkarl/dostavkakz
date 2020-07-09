from django.db import models
from user_auth.models import User
import numpy as np

slug_help_text = "Слаг - это короткая метка для представления страницы в URL. \
Содержит только буквы, цифры, подчеркивания или дефисы."


class FoodCategory(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Store(models.Model):
    # category = models.ForeignKey(FoodCategory, on_delete=models.DO_NOTHING, verbose_name='Категория')
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=150, null=True, help_text=slug_help_text, db_index=True, unique=True)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)
    description = models.CharField('Описание', max_length=500, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='store/')
    # category = models.ForeignKey(FoodCategory, verbose_name='Тэг', null=True, blank=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(FoodCategory, related_name='tags')
    time_open = models.TimeField('Открывается', null=True, blank=True)
    time_closed = models.TimeField('Закрывается', null=True, blank=True)
    latitude = models.CharField('Широота', max_length=50, null=True, blank=True)
    longitude = models.CharField('Высота', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведении'

    def __str__(self):
        return self.name

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(list(all_ratings))


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, verbose_name='Заведение')
    category = models.ForeignKey(FoodCategory, on_delete=models.DO_NOTHING, verbose_name='Категория')
    name = models.CharField('Название', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    description = models.CharField('Описание', max_length=100)
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d')

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
