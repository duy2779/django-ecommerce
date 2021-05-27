from .models import Order, Product
import json
def cart_total(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        cartItems = order.get_cart_items
        cartAmount = order.get_cart_amount
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart:',cart)
        order = {'get_cart_total':0, 'get_cart_items':0, 'get_cart_amount':0}
        cartItems = order['get_cart_items']
        cartAmount = order['get_cart_amount']

        for i in cart:
            cartItems += cart[i]['quantity']
            price = Product.objects.values_list('price',flat=True).get(id=i)
            cartAmount += cartItems*price
    return {'cartItems':cartItems, 'cartAmount':cartAmount}

def order_total(request):
    total = 0
    if request.user.is_authenticated:
        total = Order.objects.filter(customer=request.user.customer, status=1).count()
    return {'order_item':total}
