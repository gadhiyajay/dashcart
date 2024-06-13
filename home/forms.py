from django import forms
from .models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'categories', 'price', 'stock', 'image']
        
class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['title', 'description', 'category_image', 'parent']