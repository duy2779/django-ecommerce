from django.http import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff == 1:
            return redirect('admin:dashboard')
        if request.user.is_authenticated and request.user.is_staff == 0:
            return HttpResponse("Bạn không được phép truy cập phần này, vui lòng đăng xuất tài khoản khách và đăng nhập tài khoản nhân viên để truy cập!")
        return view_func(request, *args, **kwargs)
    return wrapper_func

