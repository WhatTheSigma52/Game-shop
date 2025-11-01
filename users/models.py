from django.db import models
from django.contrib.auth.models import User
from games.models import Order, Game


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                default='random_user')
    about = models.TextField(max_length=500,
                             default='Ничего',
                             verbose_name='О себе')
    birth_date = models.DateField(default='2000-01-01',
                                  verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='avatars/',
                               default='default/default.jpg',
                               verbose_name='Аватар')

    def __str__(self):
        return self.user.username

    @property
    def library(self):
        from django.db.models import Prefetch
        completed_orders = Order.objects.filter(user=self.user, status='Completed')
        games = Game.objects.filter(order__in=completed_orders).distinct(games)
        return games