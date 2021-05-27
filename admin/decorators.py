from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff == 1:
            return redirect('admin:dashboard')
        if request.user.is_authenticated and request.user.is_staff == 0:
            return HttpResponse("Bạn không được phép truy cập phần này, vui lòng đăng xuất tài khoản khách và đăng nhập tài khoản nhân viên để truy cập!")
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Not allowed")
        return wrapper_func
    return decorator



class SuperUserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse("Bạn không có quyền truy cập phần này")
        return super(SuperUserRequiredMixin, self).dispatch(request,
            *args, **kwargs)