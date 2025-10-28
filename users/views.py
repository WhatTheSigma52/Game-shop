from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm


class SighUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('games:index')
    template_name = 'users/signup.html'

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)

    from games.models import Order
    library_games = []
    completed_orders = Order.objects.filter(user=request.user, status='Completed')
    
    for order in completed_orders:
        for game in order.games.all():
            library_games.append({
                'game': game,
                'purchase_date': order.date
            })
    
    context = {
        'profile': profile,
        'form': form,
        'library_games': library_games,
    }
    return render(request, 'users/profile.html', context)