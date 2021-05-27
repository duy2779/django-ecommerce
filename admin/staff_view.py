from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, SuperUserRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test

from store.models import User, Customer
from django.views import View


def staffs(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    if not request.user.is_superuser:
        return HttpResponse("Bạn không có quyền truy cập phần này")
    staffs = User.objects.filter(is_staff=1)
    context = {'staffs':staffs}
    return render(request, 'admin/staff/index.html', context)

class StaffAdd(LoginRequiredMixin,SuperUserRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'admin/staff/add.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        if re_password != password:
            messages.error(request,'Mật khẩu nhập lại không trùng khớp')
            return redirect('admin:staff_add')
        if User.objects.filter(username=username):
            messages.error(request,'Tên tài khoản đã tồn tại')
            return redirect('admin:staff_add')
        user = User.objects.create(username=username, password=make_password(password), email=email, first_name=name, is_staff=1, is_active=1)
        Customer.objects.create(name=name, email=email, user=user)
        messages.success(request,'Thêm 1 nhân viên thành công')
        return redirect('admin:staffs')

class StaffDelete(LoginRequiredMixin,SuperUserRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        try:
            staff = User.objects.get(id=id)
        except:
            messages.error(request,'Nhân viên không tồn tại')
            return redirect('admin:staffs')
        context = {'staff':staff}
        return render(request, 'admin/staff/delete.html', context)

    def post(self, request, id):
        try:
            staff = User.objects.get(id=id)
        except:
            messages.error(request,'Nhân viên không tồn tại')
            return redirect('admin:staffs')
        staff.delete()
        messages.success(request,'Xóa "'+staff.first_name+'" thành công')
        return redirect('admin:staffs')