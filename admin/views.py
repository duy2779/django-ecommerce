from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.admin.views.decorators import staff_member_required
from store.models import *
from django.views import View

# Create your views here.
@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff == True:
                login(request, user)
                return redirect('admin:dashboard')
            else:
                messages.error(request,'Nhập tài khoản nhân viên hoặc admin, tài khoản khách hàng không được quyền truy cập vào hệ thống')
        else:
            messages.error(request,'Tên tài khoản hoặc mật khẩu không đúng')
    return render(request,'admin/login/login.html')


def logoutUser(request):
    logout(request)
    return redirect('admin:login')


@staff_member_required(login_url='admin:login')
def dashboard(request):
    product_total = Product.objects.filter(status=1).count()
    orders = Order.objects.filter(status=2)
    quantity_total = sum([item.get_cart_items for item in orders])
    orders_not_checked = Order.objects.filter(status=1).count()
    members = Customer.objects.exclude(user__isnull=True).count()
    context = {'product_total':product_total, 'quantity_total':quantity_total, 'orders_not_checked':orders_not_checked, 'members':members}
    return render(request, 'admin/dashboard/dashboard.html', context)






