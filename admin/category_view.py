from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user, allowed_users
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from store.models import *
from django.views import View
from django.template.defaultfilters import slugify

@staff_member_required(login_url='admin:login')
def categories(request):
    categories = Category.objects.exclude(status=0)
    context = {'categories':categories}
    return render(request, 'admin/category/index.html' , context)

@staff_member_required(login_url='admin:login')
def categories_trash(request):
    categories = Category.objects.filter(status=0)
    context = {'categories':categories}
    return render(request, 'admin/category/trash.html' , context)

@staff_member_required(login_url='admin:login')
def category_status(request, id):
    try:
        category = Category.objects.get(id=id)
        if category.status == 1:
            category.status = 2
        else:
            category.status = 1
        category.save()
        messages.success(request,'Thay đổi trạng thái thành công')
    except:
        messages.error(request,'Loại sản phẩm không tồn tại')
    return redirect('admin:categories')

@staff_member_required(login_url='admin:login')
def category_deltrash(request, id):
    try:
        category = Category.objects.get(id=id)
        category.status = 0
        category.save()
        messages.success(request,'Xóa vào thùng rác thành công')
    except:
        messages.error(request,'Loại sản phẩm không tồn tại')
    return redirect('admin:categories')

@staff_member_required(login_url='admin:login')
def category_retrash(request, id):
    try:
        category = Category.objects.get(id=id)
        category.status = 2
        category.save()
        messages.success(request,'Khôi phục thành công')
    except:
        messages.error(request,'Loại sản phẩm không tồn tại')
    return redirect('admin:categories_trash')

@method_decorator(staff_member_required, name='dispatch')
class CategoryAdd(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        categories = Category.objects.filter(status=1)
        context = {'categories':categories}
        return render(request, 'admin/category/add.html', context)

    def post(self, request):
        name = request.POST.get('name')
        parent_id = request.POST.get('parent-id')
        if parent_id =='':
            parent = None
        else:
            parent = Category.objects.get(id=parent_id)
        order = int(request.POST.get('order')) + 1
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if Category.objects.filter(slug=slug).count() > 0:
            messages.error(request,'Tên loại sản phẩm đã tồn tại')
            return redirect('admin:category_add')
        else:
            Category.objects.create(name=name, parent_id=parent, slug=slug, order=order, created_by=user, updated_by=user, status=status)
            messages.success(request,'Thêm "'+name+'" thành công')
            return redirect('admin:categories')


@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdate(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except:
            messages.error(request,'Loại sản phẩm không tồn tại')
            return redirect('admin:categories')
        try:
            order = Category.objects.get(order=category.order-1)
        except:
            order = {}
        categories = Category.objects.filter(status=1).exclude(id=category.id)
        context = {'categories':categories, 'category':category, 'order':order}
        return render(request, 'admin/category/edit.html', context)

    def post(self, request, slug):
        category = Category.objects.get(slug=slug)
        name = request.POST.get('name')
        parent_id = request.POST.get('parent-id')
        if parent_id =='':
            parent = None
        else:
            parent = Category.objects.get(id=parent_id)
        if int(request.POST.get('order')) == category.order:
            order = int(request.POST.get('order'))
        else:
            order = int(request.POST.get('order')) + 1
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if name != category.name:
            if Category.objects.filter(slug=slug).count() > 0:
                messages.error(request,'Tên loại sản phẩm đã tồn tại')
                return redirect('admin:category_update', slug=category.slug)
            else:
                category.name = name
        category.parent_id = parent
        category.order = order
        category.slug = slug
        category.status = status
        category.created_by = user
        category.updated_by = user
        category.save()
        messages.success(request,'Cập nhật"'+name+'" thành công')
        return redirect('admin:categories')

@method_decorator(staff_member_required, name='dispatch')
class CategoryDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except:
            messages.error(request,'Loại sản phẩm không tồn tại')
            return redirect('admin:categories_trash')
        context = {'category':category}
        return render(request, 'admin/category/delete.html', context)

    def post(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except:
            messages.error(request,'Loại sản phẩm không tồn tại')
            return redirect('admin:categories_trash')
        category.delete()
        messages.success(request,'Xóa "'+category.name+'" thành công')
        return redirect('admin:categories_trash')