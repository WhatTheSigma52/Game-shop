from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.mail import send_mail
from django.conf import settings
from games.models import Game, Cart, Order, Review, Genre
from users.models import Profile
from games.forms import ReviewForm
from django.contrib.auth import get_user_model
from games.models import Order
import logging


logger = logging.getLogger(__name__)
User = get_user_model()


def index(request):
    games = Game.objects.all()
    genres = Genre.objects.all().order_by('name')

    query = request.GET.get('q')
    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(developer__icontains=query)) 

    filter_type = request.GET.get('filter')
    if filter_type == 'price_asc':
        games = games.order_by('price')
    elif filter_type == 'price_desk':
        games = games.order_by('-price')
    elif filter_type == 'popular':
        games = games.annotate(review_count=Count('reviews')).order_by('-review_count')

    genre = request.GET.get('genre')
    if genre:
        games = games.filter(genres__name=genre)

    context = {'games': games, 'genres': genres}
    return render(request, 'games/home.html', context)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    print(f'Страница игры {game.title} загружена')
    in_cart = False
    in_library = False
    user_review = None

    if request.user.is_authenticated:
        print(f'Нашел пользователя {request.user.username}')
        try:
            cart = Cart.objects.get(user=request.user)
            in_cart = cart.games.filter(pk=game_id).exists()
            print(f'Игра в корзине {in_cart}')
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            in_cart = False
        in_library = Order.objects.filter(user=request.user,
                                        status='Completed',
                                        games=game).exists()
        print(f'Игра в библиотеке {in_library}')
        if in_library:
            try:
                user_review = Review.objects.filter(user=request.user,
                                                    game=game).first()
                print(f'Отзыв пользователя {user_review} найден')
            except Review.DoesNotExist:
                user_review = None
                print(f'У пользователя нет отзыва')

    if request.method == 'POST' and in_library:
        if user_review:
            form = ReviewForm(request.POST,
                              instance=user_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
            return redirect('games:game_detail', game_id=game_id)

    else:
        if user_review:
            form = ReviewForm(instance=user_review)
        else:
            form = ReviewForm()

    reviews = game.reviews.all()
    context = {'game': game,
               'reviews': reviews,
               'form': form,
               'in_cart': in_cart,
               'in_library': in_library,
               'user_review': user_review}
    return render(request, 'games/game_detail.html', context)


@login_required
def cart(request):
    cart = request.user.cart
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context)


@login_required
def delete_from_cart(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    cart = request.user.cart
    cart.games.remove(game)
    return redirect('games:cart')


def add_to_cart(request, game_id):
    logger.info(f'add_to_cart вызвана пользователем {request.user} для игры {game_id}')
    print(f'add_to_cart вызвана пользователем {request.user} для игры {game_id}')
    game = get_object_or_404(Game, pk=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.games.filter(pk=game.id).exists():
        cart.games.add(game)
    return redirect('games:cart')


@login_required
def make_order(request):
    cart = request.user.cart
    if not cart.games.exists():
        return redirect('games:cart')
    if request.method != 'POST':
        return redirect('games:cart')
    order = Order.objects.create(user=request.user, total_price=cart.count_price())
    print(f'Начал обрабатывать заказ {order.id}')
    for game in cart.games.all():
        order.games.add(game)
    game_titles = ', '.join([game.title for game in order.games.all()])
    msg = f'Вы купили {game_titles} за {order.total_price}. Спасибо Вам за покупку!'
    send_mail('Ваша покупка в Starshop',
                msg,
                'starshop@email.',
                [request.user.email],
                False)
    return redirect('games:order_success', order.id)


@login_required
def checkout(request):
    cart = request.user.cart
    if not cart.games.exists():
        return redirect('games:cart')
    context = {'cart': cart}
    return render(request, 'cart/order.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    cart = request.user.cart
    cart.games.clear()
    order.status = 'Completed'
    order.save()
    context = {'order': order}
    return render(request, 'cart/order_success.html', context)


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    library_games = []
    completed_orders = Order.objects.filter(user=request.user, status='Completed')

    for order in completed_orders:
        for game in order.games.all():
            library_games.append({
                'game': game,
                'purchase_date': order.date})

    is_own_profile = request.user == user

    context = {'user': user,
               'profile': profile,
               'library_games': library_games,
               'is_own_profile': is_own_profile}
    return render('games/public_profile.html', context)