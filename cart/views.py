from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import CartItem, Product
from django.db.models import Sum, F
# Create your views here.


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # aggregate_query(for total price)
    total_price = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total']    
    return render(request, 'cart/cart_list.html', {'cart_items' : cart_items, 'total_price' : total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def update_cart_quantity(request, item_id, action):
    if action not in ['increase', 'decrease']:
        return HttpResponse('not_allowed')
    
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.quantity = 1    
    cart_item.save()
    return redirect('view_cart')




