from django import forms
from .models import ProductCategory, Products, Featured_Products

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category_name', 'cat_image']

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'category', 'sub_category', 'price', 'stock', 'desc', 'prd_image']

class FeaturedProductsForm(forms.ModelForm):
    class Meta:
        model = Featured_Products
        fields = ['product_name', 'category', 'product', 'sub_category', 'price', 'stock', 'desc', 'prd_image']
