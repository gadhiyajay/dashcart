from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from .forms import ProductForm, CategoryForm
from users.models import Profile
# Create your views here.


def category_view(request):
    parent_category = Category.objects.filter(parent__isnull=True)
    return render(request, 'home/category_list.html', {'categories': parent_category})

def subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategory = Category.objects.filter(parent=category)
    return render(request, 'home/subcategory_list.html', {'categories': category,'subcategories': subcategory})

def product_view(request, subcategory_id):
    subcategory = get_object_or_404(Category, id=subcategory_id)
    products = Product.objects.filter(categories=subcategory)
    return render(request, 'home/product_list.html', {'subcategory': subcategory, 'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the product list or any other page
    else:
        form = ProductForm()
    return render(request, 'home/product_add.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'home/category_add.html', {'form' : form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    subcategory = product.categories.first()  # Handle many-to-many relationship
    if subcategory:
        subcategory_id = subcategory.id
    else:
        subcategory_id = None
    product.delete()
    if subcategory_id:
        return redirect('product_list', subcategory_id=subcategory_id)
    else:
        return redirect('category_list')
            
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    subcategory = product.categories.first()
    if subcategory:
        subcategory_id = subcategory.id
    else:
        subcategory_id = None
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', subcategory_id=subcategory_id)
    return render(request, 'product_edit.html', {'form': form, 'product': product})

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_details.html', {"product":product})