from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact_us'),
    path('api/suggestions/', views.autocomplete_suggestions, name='autocomplete_suggestions'),
    path('store/', views.store, name='store'),
    path('product_details/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('create_razorpay_order/<int:order_id>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment_status/', views.payment_status, name='payment_status'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    
    path('order_history/', views.order_history, name='order_history'),
    path('invoice/<int:order_id>/', views.invoice_view, name='invoice'),
    
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('manage_reviews/', views.manage_reviews, name='manage_reviews'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    
]
