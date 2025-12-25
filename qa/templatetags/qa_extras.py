from django import template
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('includes/right_sidebar.html')
def right_sidebar():
    tags = cache.get('popular_tags', [])
    users = cache.get('best_users', [])
    return {'popular_tags': tags, 'best_users': users}
