from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug':('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'in_stock', 'is_available', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ['price', 'in_stock']