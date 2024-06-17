from django.contrib import admin
from .models import Products, ProductImages, ProductDetails, Order, Cart, CartItems, ProductReview, Wishlist, BannerPage, OrderItems

class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class ProductDetailsInline(admin.StackedInline):
    model = ProductDetails

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'prd_image', 'price', 'max_retail_price', 'stock', 'featured', 'in_stock']
    list_filter = ['category', 'featured', 'in_stock']
    search_fields = ['product_name', 'description']
    inlines = [ProductImagesInline, ProductDetailsInline]
    
admin.site.register(Products, ProductsAdmin)

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0
    readonly_fields = ['order', 'product', 'quantity'] 
    can_delete = False 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_email', 'order_status', 'payment_status', 'payment_mode', 'order_date', 'products_list')
    list_filter = ['order_status', 'payment_status', 'payment_mode', 'order_date']
    search_fields = ['cart__user__email', 'cart__cart_items__product__product_name']
    inlines = [OrderItemsInline]

    def user_email(self, obj):
        return obj.cart.user.email
    user_email.short_description = 'User Email'
    
    def products_list(self, obj):
        order_items = obj.order_items.all() if obj.order_items.exists() else None
        if order_items:
            product_details = [f"{item.product.product_name} (Qty: {item.quantity})" for item in order_items]
            return ", ".join(product_details)
        else:
            return "No products ordered"
    products_list.short_description = 'Products Ordered'

    # Customize the view when clicking on an order ID
    def view_on_site(self, obj):
        return f"/admin/products/order/{obj.pk}/change/"  # Replace 'orders' with your app name

admin.site.register(Order, OrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')

admin.site.register(Cart, CartAdmin)

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total')

admin.site.register(CartItems, CartItemsAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating', 'date']
    list_filter = ['rating', 'date']
    search_fields = ['user__username', 'product__product_name']
    
admin.site.register(ProductReview, ProductReviewAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    search_fields = ['user__username', 'product__product_name']
    
admin.site.register(Wishlist, WishlistAdmin)

class BannerPageAdmin(admin.ModelAdmin):
    list_display = ['mainTitle', 'subTitle', 'short_desc']
    search_fields = ['mainTitle', 'subTitle', 'short_desc']

admin.site.register(BannerPage, BannerPageAdmin)
