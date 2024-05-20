from django.shortcuts import render, redirect
from .models import Category, SubCategory, Products
from django import forms

# Create your views here.

def category_view(request):
    categories = Category.objects.all()
    return render(request, 'home/category_list.html', {'categories': categories})

def subcategory_view(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'home/subcategory_list.html', {'subcategories': subcategories})

def product_view(request):
    products = Products.objects.all()
    return render(request, 'home/product_list.html', {'products': products})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['title', 'description', 'categories', 'price', 'stock', 'image']

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list or any other page
    else:
        form = ProductForm()
    return render(request, 'home/product_add.html', {'form': form})