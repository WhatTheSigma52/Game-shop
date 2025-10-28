from django.contrib import admin
from .models import Game, SystemRequirements, Genre, OperationSystem, Order



class SystemRequirementsInline(admin.StackedInline):
    model = SystemRequirements
    can_delete = False


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [SystemRequirementsInline]
    list_display = ('title',
                    'pk',
                    'price',
                    'developer',
                    'release_year')
    search_fields = ('title', 'developer')
    list_filter = ('release_year',)
    list_editable = ('price',)
    empty_value_display = '~empty~'


@admin.register(SystemRequirements)
class SystemRequirementsAdmin(admin.ModelAdmin):
    list_display = ('game','cpu', 'ram', 'gpu', 'os')
    search_fields = ('game__title',)
    list_filter = ('game__release_year',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_price', 'date')
    search_fields = ('user__username',)
    list_filter = ('status',)


admin.site.register(Genre)
admin.site.register(OperationSystem)
