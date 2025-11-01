from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def stars_display(rating):
    if rating is None:
        rating = 0
    stars = []
    for i in range(1, 6):
        if rating >= i:
            stars.append('full')
        elif rating >= i - 0.5:
            stars.append('half')
        else:
            stars.append('empty')
    return stars


@register.filter
def format_rating(rating):
    if rating is None:
        return '0.0'
    return f'{rating:.1f}'
