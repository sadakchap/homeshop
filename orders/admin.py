from django.contrib import admin
from .models import Order, OrderItem, Address

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class AddressAdmin(admin.StackedInline):
    model = Address
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [AddressAdmin, OrderItemInline]
