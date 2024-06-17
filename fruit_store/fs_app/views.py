from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from products.models import Products, Cart, CartItems, Order, ProductDetails, ProductImages, CheckoutAddress, OrderItems, BannerPage, ProductReview
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.core.paginator import Paginator
from authentication.models import User, Address
from django.http import JsonResponse
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from django.db import IntegrityError
import razorpay 
from django.conf import settings
from django.db.models import F
from django.db.models import Q
from django.db import transaction
import random
from fs_app.utils.pdf import render_to_pdf

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def index(request):
    products = Products.objects.all()
    banner_page = BannerPage.objects.first()
    
    product_reviews = ProductReview.objects.select_related('product').filter(product__in=products)
    
    if banner_page:
        main_title_parts = banner_page.mainTitle.split()
        first_two_words = " ".join(main_title_parts[:2])
        remaining_words = " ".join(main_title_parts[2:])
        
        banner_product = banner_page.products.first() if banner_page.products.exists() else None
        discount_percentage = banner_product.get_percentage() if banner_product else 0

        context = {
            "products": products,
            "banner_page": banner_page,
            "first_two_words": first_two_words,
            "remaining_words": remaining_words,
            "banner_product": banner_product,
            "discount_percentage": discount_percentage,
            "product_reviews": product_reviews,
        }
    else:
        context = {
            "products": products,
            "banner_page": None,
            "first_two_words": None,
            "remaining_words": None,
            "banner_product": None,
            "discount_percentage": 0,
            "product_reviews": product_reviews,
        }
        
    return render(request, "home/index.html", context)

def about(request):
    return render(request, 'home/about.html')

def contact_us(request):
    return render(request, 'home/contact.html')

def privacy_policy(request):
    return render(request, 'home/privacy-policy.html')

def autocomplete_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        products = Products.objects.filter(Q(product_name__icontains=query) | Q(category__icontains=query))
        suggestions = [{'name': product.product_name} for product in products]
    
    # Print statements for debugging
    print(f"Query: {query}")
    print(f"Suggestions: {suggestions}")

    return JsonResponse(suggestions, safe=False)

def store(request):
    context = {}
    sort_by = request.GET.get('sort', 'default')
    search_query = request.GET.get('search', '')

    products = Products.objects.all().select_related('details')
    
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(category__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if sort_by == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'latest':
        products = products.order_by('-details__Date_of_manufacturing')
    elif sort_by == 'expiry_date':
        products = products.order_by('details__Date_of_Expiry')
    # Add the following block to apply the search filter even when sort is 'default'
    elif sort_by == 'default':
        if search_query:
            products = products.filter(
                Q(product_name__icontains=search_query) | 
                Q(category__icontains=search_query) |
                Q(description__icontains=search_query)
            )
    
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number)

    context["products"] = paginated_products
    context["all_products"] = products
    context["search_query"] = search_query
    context["sort_by"] = sort_by
    
    return render(request, "store/products.html", context)

class ProductDetailView(View):
    def get(self, request, product_id):
        fproducts = Products.objects.all()
        
        user = request.user
        
        product = get_object_or_404(Products, pk=product_id)

        details = get_object_or_404(ProductDetails, product=product)

        product_images = ProductImages.objects.filter(product=product)
        
        if request.user.is_authenticated:
            existing_review = ProductReview.objects.filter(user=request.user, product=product).first()
        else:
            existing_review = None 
        
        # Find related products based on keywords
        keywords = product.product_name.split()
        related_products = Products.objects.none()
        for keyword in keywords:
            related_products |= Products.objects.exclude(pk=product_id).filter(product_name__icontains=keyword)
            
        # Remove duplicate related products if any
        related_products = related_products.distinct()    
            
        context = {
            'fproducts': fproducts,
            'product': product,
            'details': details,
            'product_images': product_images,
            'related_products': related_products,
            'existing_review': existing_review,
        }
        return render(request, 'store/product_details.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.total = cart_item.quantity * product.price
    cart_item.save()
    messages.success(request, f"{product.product_name} added to cart.")

    data = {
        'cart_count': cart.cart_items.count(),
        'message': f"{product.product_name} added to cart."
    }
    return JsonResponse(data)

@login_required
def cart_detail(request):
    user = request.user
    cart_items = CartItems.objects.filter(cart__user=user)

    # Ensure all necessary attributes are calculated for each cart item
    total_mrp = 0
    total_discount = 0
    total_amount = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total_mrp += item.product.max_retail_price * item.quantity
        total_discount += (item.product.max_retail_price - item.product.price) * item.quantity
        total_amount += item.total_price
        item.unit_parameter = ProductDetails.objects.get(product=item.product).unit_parameter

    # Calculate tax for the total price
    tax_percentage = 0.12  # 12% tax rate
    tax_amount = total_amount * tax_percentage

    # Calculate the total price including tax
    total_price_with_tax = total_amount + tax_amount
    
    # Check if the cart is empty
    is_cart_empty = not cart_items.exists()
    
    cart_detail_url = reverse('cart_detail')

    context = {
        'cart_items': cart_items,
        'user': user,
        'total_mrp': total_mrp,
        'total_discount': total_discount,
        'total_amount': total_amount,
        'tax_amount': tax_amount,
        'total_price_with_tax': total_price_with_tax,
        'is_cart_empty':is_cart_empty,
        'cart_detail_url':cart_detail_url,
    }

    return render(request, 'store/cart_detail.html', context)

@login_required
def clear_cart(request):
    CartItems.objects.filter(cart__user=request.user).delete()
    return redirect('cart_detail') 

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': f'{cart_item.product.product_name} has been removed from the cart.'})

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.total = cart_item.quantity * cart_item.product.price
    cart_item.save()
    return redirect('cart_detail')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total = cart_item.quantity * cart_item.product.price
        cart_item.save()
    return redirect('cart_detail')

@login_required
def buy_now(request, product_id):
    user = request.user
    product = get_object_or_404(Products, id=product_id)

    # Generate a new order ID every time user proceeds to checkout
    order_id = generate_order_id()

    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item, item_created = CartItems.objects.get_or_create(cart=cart, product=product)

    if item_created:
        cart_item.quantity = 1
    cart_item.total = cart_item.quantity * product.price
    cart_item.save()

    total_amount = cart_item.total
    unit_parameter = ProductDetails.objects.get(product=product).unit_parameter
    total_mrp = product.max_retail_price * cart_item.quantity
    total_discount = (product.max_retail_price - product.price) * cart_item.quantity
    tax_percentage = 0.12
    tax_amount = total_amount * tax_percentage
    total_price_with_tax = total_amount + tax_amount
    address, created = Address.objects.get_or_create(user=user)

    if request.method == 'POST':
        checkout_address = CheckoutAddress(
            user=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            street1=request.POST.get('street1'),
            street2=request.POST.get('street2'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('zip_code'),
            additional_msg=request.POST.get('additional_msg')
        )
        checkout_address.save()

        try:
            order, created = Order.objects.get_or_create(
                user=user,
                order_id=order_id,  # Assign the generated order ID
                cart=cart,
                defaults={'checkoutAddress': checkout_address, 'payment_mode': 'upi'}
            )

            if not created:
                order.checkoutAddress = checkout_address
                order.save()

            OrderItems.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': cart_item.quantity}
            )

            return redirect('create_razorpay_order', order_id=order.order_id)

        except IntegrityError:
            order = Order.objects.get(user=user, cart=cart)
            order.checkoutAddress = checkout_address
            order.save()

            order_item, item_created = OrderItems.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': cart_item.quantity}
            )

            if not item_created:
                order_item.quantity = cart_item.quantity
                order_item.save()

            return redirect('create_razorpay_order', order_id=order.order_id)

    context = {
        'cart_items': [cart_item],
        'user': user,
        'address': address,
        'unit_parameter': unit_parameter,
        'total_amount': total_amount,
        'is_buy_now': True,
        'total_discount': total_discount,
        'total_mrp': total_mrp,
        'tax_amount': tax_amount,
        'total_price_with_tax': total_price_with_tax,
        'checkout_url': reverse('buy_now', kwargs={'product_id': product_id}),
    }

    return render(request, 'store/checkout.html', context)

# Function to generate a new unique order ID
def generate_order_id():
    return str(random.randint(100000, 999999))  # Random 6-digit number

@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = cart.cart_items.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    total_mrp = sum(item.product.max_retail_price * item.quantity for item in cart_items)
    total_discount = sum((item.product.max_retail_price - item.product.price) * item.quantity for item in cart_items)
    tax_percentage = 0.12
    tax_amount = total_amount * tax_percentage
    total_price_with_tax = total_amount + tax_amount

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.unit_parameter = ProductDetails.objects.get(product=item.product).unit_parameter

    address, created = Address.objects.get_or_create(user=user)

    if request.method == 'POST':
        checkout_address = CheckoutAddress(
            user=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            street1=request.POST.get('street1'),
            street2=request.POST.get('street2'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('zip_code'),
            additional_msg=request.POST.get('additional_msg')
        )
        checkout_address.save()

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                cart=cart,
                checkoutAddress=checkout_address,
                payment_mode='upi'
            )

            for cart_item in cart_items:
                OrderItems.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

        return redirect('create_razorpay_order', order_id=order.order_id)

    context = {
        'cart_items': cart_items,
        'user': user,
        'address': address,
        'total_amount': total_amount,
        'total_discount': total_discount,
        'total_mrp': total_mrp,
        'tax_amount': tax_amount,
        'total_price_with_tax': total_price_with_tax,
        'checkout_url': reverse('checkout'),
    }

    return render(request, 'store/checkout.html', context)

def create_razorpay_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    # Calculate total price with tax
    order_items = OrderItems.objects.filter(order=order)
    total_amount = sum(item.product.price * item.quantity for item in order_items)
    tax_percentage = 0.12  # 12% tax rate
    tax_amount = total_amount * tax_percentage
    total_price_with_tax = total_amount + tax_amount

    # Generate a unique order ID with 6 digits
    unique_order_id = str(random.randint(100000, 999999))  # Random 6-digit number

    data = {
        "amount": int(total_price_with_tax * 100),  # Amount in paise
        "currency": "INR",
        "receipt": unique_order_id,  # Use the generated unique order ID as the receipt
        "payment_capture": 1
    }

    try:
        razorpay_order = client.order.create(data=data)
        order.razorpay_order_id = razorpay_order.get('id')
        order.save()

        # Reduce the stock of each product in the order by the ordered quantity
        for order_item in order_items:
            product = order_item.product
            product.stock -= order_item.quantity
            product.save()

        context = {
            "order_id": razorpay_order.get('id'),
            "amount": int(total_price_with_tax * 100),
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "callback_url": reverse('payment_status'),
            "order": order,
        }

        return render(request, 'orders/payment.html', context)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def payment_status(request):
    if request.method == "POST":
        params_dict = {
            'razorpay_order_id': request.POST.get('razorpay_order_id', ''),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id', ''),
            'razorpay_signature': request.POST.get('razorpay_signature', '')
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            order.razorpay_payment_id = params_dict['razorpay_payment_id']
            order.razorpay_signature = params_dict['razorpay_signature']
            order.payment_status = True
            order.order_status = 'Processing'
            order.save()

            order.cart.cart_items.all().delete()

            context = {
                'status': 'Payment successful',
                'order': order
            }

            return render(request, 'orders/payment_status.html', context)
        except Exception as e:
            context = {
                'status': 'Payment failed',
                'order': order,
                'error': str(e)
            }
            return render(request, 'orders/payment_status.html', context)

    return redirect('checkout')

@login_required
def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.order_items.all()
    
    for item in items:
        item.total_price = item.quantity * item.product.price
        item.unit_parameter = ProductDetails.objects.get(product=item.product).unit_parameter
    
    subtotal = sum(item.total_price for item in items)
    tax_rate = 12  # Example tax rate
    tax = subtotal * 0.12
    total = subtotal + tax
    
    # Prepare the context to be passed to the template
    context = {
        'order': order,
        'items': items,
        'user': request.user,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total,
    }
    
    # Render the invoice template with the provided context
    return render(request, 'orders/invoice.html', context)


@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.order_items.all()
    
    for item in items:
        item.total_price = item.quantity * item.product.price
        item.unit_parameter = ProductDetails.objects.get(product=item.product).unit_parameter
        
    subtotal = sum(item.total_price for item in items)
    tax_rate = 12  
    tax = subtotal * (tax_rate / 100)
    total = subtotal + tax
    
    context = {
        'order': order,
        'items': items,
        'user': request.user,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total,
    }
    pdf = render_to_pdf('orders/downlodable_invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order.order_id}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__product')
    order_data = []

    for order in orders:
        items = order.order_items.all()
        item_data = []
        total_order_price = 0

        for item in items:
            total_price = item.quantity * item.product.price
            total_order_price += total_price
            item_data.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': total_price
            })

        order_data.append({
            'order': order,
            'items': item_data,
            'rowspan': len(items) + 1,
            'total_order_price': total_order_price
        })
    
    context = {'order_data': order_data}
    return render(request, 'orders/orders.html', context)


# Views for Submiting reviews...---------------------------

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    user = request.user

    existing_review = ProductReview.objects.filter(user=user, product=product).first()

    if request.method == 'POST':
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')

        if existing_review:
            existing_review.rating = rating
            existing_review.review = review_text
            existing_review.save()
            messages.success(request, "Your review has been updated.")
        else:
            new_review = ProductReview(
                user=user,
                product=product,
                rating=rating,
                review=review_text 
            )
            new_review.save()
            messages.success(request, "Your review has been submitted.")

        return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'existing_review': existing_review,
    }

    return render(request, 'store/submit_review.html', context)

@login_required
def manage_reviews(request):
    user = request.user
    products = Products.objects.all()
    
    if not user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('index')

    reviews = ProductReview.objects.all()
    context = {
        'reviews': reviews,
        'products':products
    }
    return render(request, 'store/manage_reviews.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)

    if request.user.is_staff or review.user == request.user: 
        review.delete()
        messages.success(request, "Review has been deleted.")
    else:
        messages.error(request, "You do not have permission to delete this review.")

    return redirect('manage_reviews')