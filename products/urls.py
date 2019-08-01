from django.urls import path
from .views import product_list, product_detail
app_name = 'products'

urlpatterns = [
    path('', product_list, name='list'),
    path('<slug:cat_slug>/', product_list, name='list_by_category'),
    path('<slug:slug>/detail/', product_detail, name='prod_detail'),
]