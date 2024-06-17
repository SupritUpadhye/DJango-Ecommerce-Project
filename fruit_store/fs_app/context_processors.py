from django.db.models import Sum
from products.models import Cart, ProductDetails

def cart_items(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)
            cart_items = cart.cart_items.all()

            # Calculate total price
            total_price = cart_items.aggregate(total=Sum('total'))['total'] or 0

            # Retrieve unit_parameter for each product
            for item in cart_items:
                try:
                    item.unit_parameter = ProductDetails.objects.get(product=item.product).unit_parameter
                except ProductDetails.DoesNotExist:
                    item.unit_parameter = 'unit'  # Default value if ProductDetails does not exist

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
