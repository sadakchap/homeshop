from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import OrderItem, Order
from .forms import ShippingAddresForm
from cart.cart import Cart
from .tasks import order_created_invoice

# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    addr_form = ShippingAddresForm(request.POST or None)
    if addr_form.is_valid():
        order = Order.objects.create(user=request.user)
        addr = addr_form.save(commit=False)
        addr.order = order
        addr.save()
        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'], 
                price=item['price'], 
                quantity=item['quantity']
            )
        cart.clear()
        order_created_invoice.delay(order.id)
        messages.success(request, f"An Order is created with Order No. {order.id}")
        return render(request, 'orders/order_created.html', {'order': order})

    return render(request, 'orders/order_create.html', {'addr_form': addr_form, 'cart': cart})
        