from django.db import models
from authentication.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
import random

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

CATEGORY_CHOICE = (
    ('fruits', 'fruits'),
    ('vegetables', 'vegetables'),
    ('Fruit Juice', 'fruit juice'),
    ('Fruit Salad', 'fruit salad'),
    ('Vegetable juice', 'vegetable juice'),
    ('Vegetable Salad', 'vegetable salad'),
    ('other', 'other'),
)

UNIT_PARAMETER = (
    ('Kg', 'kg'),
    ('gram', 'gram'),
    ('Dozen', 'Dozen'),
    ('liter', 'liter'),
    ('Nos', 'Nos'),
    ('ml', 'ml'),
)

class BannerPage(models.Model):
    bannerImg = models.ImageField(upload_to="products/images", null=True, blank=True, default='products/fruitica.png')
    mainTitle = models.CharField(max_length=50)
    subTitle = models.CharField(max_length=70)
    short_desc = models.TextField()
    
    def __str__(self):
        return self.mainTitle

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=20)
    image = models.ImageField(upload_to="products/images", null=True, blank=True, default='products/fruitica.png')
    price = models.FloatField(default=0)
    max_retail_price = models.FloatField(default=0)
    stock = models.IntegerField()
    productQuantity = models.IntegerField()
    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    baner_page = models.ForeignKey(BannerPage, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    def __str__(self):
        return self.product_name
    
    def prd_image(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)
        else:
            default_image_url = settings.STATIC_URL + 'media/images/fruitica.png'
            return mark_safe('<img src="%s" width="50" height="50" />' % default_image_url)
    
    def get_percentage(self):
        if self.max_retail_price > 0:  
            discount = 100 - (self.price / self.max_retail_price) * 100
            return round(discount)  
        return 0

class ProductImages(models.Model):
    images = models.ImageField(upload_to="products/images", default="product.jpg")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='ProductImages')

class ProductDetails(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE, related_name='details')
    weight = models.FloatField(default=0)
    unit_parameter = models.CharField(choices=UNIT_PARAMETER, max_length=30, default="Kg")
    vendor = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    Date_of_manufacturing = models.DateTimeField(auto_now_add=True)
    Date_of_Expiry = models.DateTimeField()
    Detailed_description = models.TextField(default="txt")
    baner_page = models.OneToOneField(BannerPage, on_delete=models.CASCADE, related_name='product_details', null=True, blank=True)
    
    def __str__(self):
        return self.product.product_name + " - Details"

ORDER_STATUS = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending')
)

PAYMENT_MODE = (
    ("upi", "UPI"),
    ("Card", "Credit/ Debit Card"),
    ("cod", "Cash on Delivery"),
    ("pay_later", "Pay Later"),
)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_buy_now = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.FloatField(default=0)
    is_ordered = models.BooleanField(default=False) 
    
    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
    

import random

class Order(models.Model):
    order_id = models.PositiveIntegerField(unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='orders')
    checkoutAddress = models.ForeignKey('CheckoutAddress', on_delete=models.CASCADE, related_name='Checkout_addresses', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE, max_length=30, default="upi")
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=30, default="Pending")
    razorpay_order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = random.randint(100000, 9999999)
            while Order.objects.filter(order_id=self.order_id).exists():
                self.order_id = random.randint(100000, 9999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.order_items.all())

    @property
    def total_price_with_tax(self):
        tax_rate = 0.10  # example tax rate
        return self.total_price * (1 + tax_rate)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.product_name

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout_addresses')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    street1 = models.CharField(max_length=200)
    street2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    additional_msg = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=5)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.product_name
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.product_name
