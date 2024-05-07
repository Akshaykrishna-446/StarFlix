from django import template

register = template.Library()

@register.filter(name='ratings_filters')
def star_rating(average_rating):
    full_stars = int(average_rating)
    half_star = round(average_rating) - full_stars
    empty_stars = 5 - full_stars - half_star

    stars = '★' * full_stars + '½' * half_star + '☆' * empty_stars
    return stars
