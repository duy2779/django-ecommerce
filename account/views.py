from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from store.models import Customer, Order, Order_detail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user

# Create your views here.

def index(request):
    pass

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            messages.success(request,'Đăng kí tài khoản thành công')
            return redirect('account:sign_in')
    context = {'form':form}
    return render(request,'account/register.html', context)

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Tên tài khoản hoặc mật khẩu không đúng')
    return render(request,'account/sign_in.html')


def logoutUser(request):
    logout(request)
    return redirect('account:sign_in')


@login_required(login_url='account:sign_in')
def order(request):
    orders = Order.objects.filter(customer=request.user.customer).exclude(status=0)
    context = {'orders':orders}
    return render(request, 'account/order.html', context)

@method_decorator(staff_member_required, name='dispatch')
class OrderCancel(LoginRequiredMixin, View):
    login_url = 'account:sign_in'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.error(request,'Đơn hàng không tồn tại')
            return redirect('account:order')
        context = {'order':order}
        return render(request, 'account/order_cancel.html', context)

    def post(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.error(request,'Đơn hàng không tồn tại')
            return redirect('account:order')
        order.status=3
        order.save()
        messages.success(request,'Hủy đơn hàng "'+order.code+'" thành công')
        return redirect('account:order')


@login_required(login_url='account:sign_in')
def order_item(request, id):
    order = Order.objects.get(id=id)
    items = Order_detail.objects.filter(order=id)
    context = {'items':items , 'order':order}
    return render(request, 'account/order_item.html', context)