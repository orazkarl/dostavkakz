from django.db import models

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

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведении'

    def __str__(self):
        return self.name


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
