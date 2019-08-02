from django.conf import settings
from decimal import Decimal
from products.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                                    # add title of product 
                                    'quantity': 0,
                                    'price': str(product.price)
                                }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(i['quantity'] for i in self.cart.values() )

    def get_total_price(self):
        return sum( Decimal(i['price']) * i['quantity'] for i in self.cart.values() )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price']) # converting back to decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

            # cart = self.cart.copy()
            # cart = {
            #     '1':{
            #         'quantity': 1,
            #         'price': '400',
            #         'product': <Product object />
            #     },
            #     '45':{
            #         'quantity': 4,
            #         'price': '300',
            #         'product': <Product object/>
            #     }
            # }

            # yeilding only cart.values()
            # {
            #     'quantity': 1,
            #     'price': 400  as decimal
            #     'total_price': price * quantity,
            #     'product': <Product object 983258 />
            # } this is python dict




# self.session ={
#     'cart': {
#         '1':{
#             'quantity':1,
#             'price': '200.00'
#         },
#         '45':{
#             'quantity': 2,
#             'price': '399'
#         }
#     } JSON dict
# } JSON Format django uses JSON to serialize session data