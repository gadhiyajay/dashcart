from django.urls import path, include
from . import views

urlpatterns = [
    path('category_list/', views.category_view, name='category_list'),
    path('category/<int:category_id>/', views.subcategory_view, name='subcategory_list'),
    path('product_list/', views.product_view, name='product_list'),
    path('product_add/', views.add_product, name='add_product')
]
