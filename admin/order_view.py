from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import unauthenticated_user, allowed_users
from store.models import *
from django.views import View


@staff_member_required(login_url='admin:login')
def orders(request):
    orders = Order.objects.filter(status=1)
    context = {'orders':orders}
    return render(request, 'admin/order/index.html', context)


@staff_member_required(login_url='admin:login')
def orders_complete(request):
    orders = Order.objects.filter(status=2)
    context = {'orders':orders}
    return render(request, 'admin/order/complete.html', context)


@staff_member_required(login_url='admin:login')
def order_status(request, id):
    try:
        order = Order.objects.get(id=id)
        if order.status == 1:
            order.status = 2
            order.save()
            messages.success(request,'Thay đổi trạng thái thành công')
            return redirect('admin:orders')
        else:
            order.status = 1
            order.save()
            messages.success(request,'Thay đổi trạng thái thành công')
            return redirect('admin:orders_complete')
    except:
        messages.error(request,'Đơn hàng không tồn tại')
        return redirect('admin:orders')


@staff_member_required(login_url='admin:login')
def order_detail(request, id):
    order = Order.objects.get(id=id)
    items = Order_detail.objects.filter(order=id)
    context = {'items':items , 'order':order}
    return render(request, 'admin/order/item.html', context)