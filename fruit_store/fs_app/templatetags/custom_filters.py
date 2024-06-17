from django import template
from products.models import Products

from django.db import models
from products.models import Cart

register = template.Library()

@register.filter
def filter_category(products, category_id):
    if products is None:
        return None
    return products.filter(category=category_id)


def cart_items(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)
            cart_items = cart.cart_items.all()
            total_price = cart.cart_items.aggregate(total=models.Sum('total'))['total'] or 0
            return {
                'cart_items': cart_items,
                'total_price': total_price,
                'cart_count': cart_items.count()
            }
        except Cart.DoesNotExist:
            return {
                'cart_items': [],
                'total_price': 0,
                'cart_count': 0
            }
    return {
        'cart_items': [],
        'total_price': 0,
        'cart_count': 0
    }
