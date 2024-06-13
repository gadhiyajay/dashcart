from django.urls import path
from . import views
from users.views import *


urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('user-address/create/', UserAddressCreateView.as_view(), name='address_create'),
    path('user-address/list/', UserAddressListView.as_view(), name='address_list'),
    path('user-address/update/<int:pk>/', UserAddressUpdateView.as_view(), name='address_update'),
    path('user-address/delete/<int:pk>/', UserAddressDeleteView.as_view(), name='address_delete'),
    


]