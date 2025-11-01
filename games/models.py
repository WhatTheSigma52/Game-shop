from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone



User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=32,
                             unique=True)
    
    def __str__(self):
        return self.name


class OperationSystem(models.Model):
    name = models.CharField(max_length=32,
                            verbose_name='Название ОС')
    icon_class = models.CharField(max_length=64,
                                  verbose_name='Класс иконки')

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=256,
                             unique=True,
                             verbose_name='Название')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    developer = models.CharField(max_length=64,
                                 verbose_name='Разработчик')
    genres = models.ManyToManyField(Genre,
                                   verbose_name='Жанры')
    platforms = models.ManyToManyField(OperationSystem,
                                       verbose_name='Поддерживаемые ОС')
    release_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1990),
                                                                MaxValueValidator(2050)],
                                                    verbose_name='Год выхода')
    @property
    def rating(self):
        reviews = self.reviews.all()
        if reviews.count() > 0:
            return round(sum([review.rating for review in reviews]) / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.title


class SystemRequirements(models.Model):
    game = models.OneToOneField(Game,
                                on_delete=models.CASCADE,
                                related_name='system_requirements',
                                verbose_name='Игра')
    CPU_CHOICES = (("I5_12400F", "Intel core i5 12400F"),
                   ('I3_13400KF', 'Intel Core i3 13400KF'),
                   ('RYZEN5_3600', 'AMD Ryzen 5 3600'))
    GPU_CHOICES = (('NVIDIA_RTX4060', 'Nvidia Geforce RTX 4060'),
                ('NVIDIA_GTX1080TI', 'Nvidia GeForce GTX 1080 ti'),
                ('AMD_RX6600', 'AMD radeon RX 6600'),
                ('AMD_RX580', 'AMD radeon RX 580'))
    RAM_CHOICES = (('2', 2),
                   ('4', 4),
                   ('8', 8),
                   ('16', 16),
                   ('32', 32))
    OS_CHOICES = [
        ('Windows 10', 'Windows 10'),
        ('Windows 11', 'Windows 11'),
        ('Ubuntu 20.04', 'Ubuntu 20.04'),
        ('macOS Monterey', 'macOS Monterey')]
    cpu = models.CharField(max_length=16,
                           choices=CPU_CHOICES,
                           default='I5_12400F',
                           verbose_name='Процессор')
    ram = models.CharField(max_length=2,
                           choices=RAM_CHOICES,
                           default='4',
                           verbose_name='Кол-во оперативной памяти')
    gpu = models.CharField(max_length=24,
                           choices=GPU_CHOICES,
                           default='NVIDIA_RTX4060',
                           verbose_name='Видеокарта')
    os = models.CharField(max_length=50,
                          choices=OS_CHOICES,
                          default='Windows 10',
                          verbose_name='Операционная система')
    storage = models.CharField(max_length=16,
                               verbose_name='Место на диске')

    def __str__(self):
        return 'Системные требования'


class Review(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    game = models.ForeignKey(Game,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    text = models.CharField(max_length=512,
                            verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Время и дата')
    rating = models.DecimalField(max_digits=3,
                                 decimal_places=1,
                                 validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 verbose_name='Рейтинг')

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('user', 'game')

    def __str__(self):
        return f'Отзыв: {self.user} на игру: {self.game}'


class Cart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    games = models.ManyToManyField(Game,
                                   verbose_name='Игра')

    def count_price(self):
        return sum(game.price for game in self.games.all())

    def __str__(self):
        return f'Корзина {self.user}'


class Order(models.Model):
    STATUS_CHOICES = (['Completed', 'Завершено'],
                    ['Canceled', 'Отменено'],
                    ['Pending', 'Обрабатывается'])
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='Пользователь')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=32,
                              default='Pending',
                              verbose_name='Статус заказа')
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2)
    games = models.ManyToManyField(Game)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Заказ {self.pk}'
