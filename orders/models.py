from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
# Create your models here.

User = get_user_model()


class Order(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid    = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(i.get_cost() for i in self.items.all())

    def get_shipping_addr(self):
        return self.shipping_addr

class Address(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipping_addr')
    name        = models.CharField(max_length=100, null=True, blank=True, help_text='Shipping to? Who is it?')
    nickname    = models.CharField(max_length=100, null=True, blank=True, help_text='Internal Reference Nickname')
    addr_line_1 = models.CharField(max_length=120)
    addr_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city        = models.CharField(max_length=120)
    country     = models.CharField(max_length=120, default='India')
    state       = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.name)

    def get_short_address(self):
        name = self.name
        if self.nickname:
            name = f'{self.nickname} | {name}'
        return f'{name} {self.addr_line_1}, {self.city}'

    def get_address(self):
        return f'{self.name or " "} \n {self.addr_line_1}\n {self.addr_line_2}\n {self.city}, {self.state}\n {self.postal_code}, {self.country} '

class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    quantity    = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity



# OrdetItem -- ForeignKey to products
# Order -- User, OrderItem, address shipping address