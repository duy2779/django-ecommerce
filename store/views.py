from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from django.views import View
from .form import ContactForm
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def index(request):
    product_featured = Product.objects.filter(featured=True, status=1)
    product_sale = Product.objects.filter(price_sale__isnull=False, status=1)
    product_new = Product.objects.filter(status=1).order_by('-created_at')
    big_deal = Product.objects.filter(price_sale__isnull=False, status=1).order_by('price_sale')[:3]
    context = {'products_featured':product_featured, 'big_deal':big_deal, 'product_sale':product_sale, 'product_new':product_new}
    return render(request, 'store/index.html', context)

def cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product ID:', productId)
    print('Product ID:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status=0)

    orderItem, created = Order_detail.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_order(request):
    code = datetime.datetime.now().timestamp()
    data = json.loads(request.body)#load data from json
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.code = code
    if total == order.get_cart_total:
        order.status = 1
        order.delivery_address = data['form']['address']
    order.payment_method = 0
    if data['form']['payment'] == 'option2':
        order.payment_method = 1
    order.save()
    return JsonResponse('payment complete!', safe=False)


def product(request):
    context = {}
    return render(request, 'store/product.html', context)


class Contact(View):
    def get(self, request):
        contact = ContactForm()
        context = {'contact': contact}
        return render(request, 'store/contact.html', context)


    def post(self, request):
        c = ContactForm(request.POST)
        if c.is_valid():
            c.save()
            messages.success(request,'Gửi liên hệ thành công, chúng tôi sẽ phản hồi trong thời gian sớm nhất!')
            return redirect('/lien-he/')
        else:
            messages.error(request,'Gửi liên hệ không thành công, vui lòng nhập lại!')
            return redirect('/lien-he/')


    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Thanks"


def page_view(request, slug):
    try:
        page = Post.objects.get(type='page', slug=slug)
    except:
        page = None
    if not page:
        return HttpResponse("404")
    else:
        context = {'page':page}
        return render(request, 'store/page.html', context)


def deal(request):
    return HttpResponse("This is about deal")