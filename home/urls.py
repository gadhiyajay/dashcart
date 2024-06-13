from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('category_list/', views.category_view, name='category_list'),
    path('category_list/<int:category_id>/subcategories', views.subcategory_view, name='subcategory_list'),
    path('subcategory/<int:subcategory_id>/products/', views.product_view, name='product_list'),
    path('add/product/', views.add_product, name='add_product'),
    path('add/category/', views.add_category, name='add_category'),
    path('delete/product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit/product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/', views.product_details, name='product_details')
]

