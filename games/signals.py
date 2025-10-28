from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cart
from django.db.models.signals import post_save


User = get_user_model()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        print('Объект корзина создалась')


@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    instance.cart.save()
    print('Объект корзина сохранилась')
