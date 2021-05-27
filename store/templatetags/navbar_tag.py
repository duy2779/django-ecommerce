from django import template
from store.models import Category, Menu


register = template.Library()

@register.inclusion_tag('store/navbar.html')
def show_navbar():
    categories = Category.objects.filter(parent_id__isnull=True, status=1).order_by('order')
    menus = Menu.objects.filter(parent_id__isnull=True, status=1).order_by('order')
    return {'categories':categories, 'menus':menus}