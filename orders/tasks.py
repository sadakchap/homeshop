from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from celery import task
from .models import Order

@task
def order_created_invoice(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        # print("Problem here")
        pass
    user = order.user
    sub = f'{user}, your has been placed with Order no. {order.id}'
    msg = f'Dear {user},\n Order no. is {order.id} Thank you for shopping with us!'

    mail_sent = send_mail(sub, msg, settings.EMAIL_HOST_USER, [user.email])

    return mail_sent