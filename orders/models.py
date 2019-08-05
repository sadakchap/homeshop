from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
# Create your models here.

User = get_user_model()

class Address(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_addrs')
    line_1  = models.CharField(max_length=255)
    line_2  = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city    = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city} Zip Code {self.postal_code}'



class Order(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # items   = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_item')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid    = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(i.get_cost() for i in self.items.all())

class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    products    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    quantity    = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity



# OrdetItem -- ForeignKey to products
# Order -- User, OrderItem, address shipping address