from django.urls import path
from . import views

app_name = 'games'


urlpatterns = [
    path('', views.index, name='index'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/<int:game_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('cart/add/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/make_order/', views.make_order, name='make_order'),
    path('cart/<int:order_id>/order_success/', views.order_success, name='order_success'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
]
