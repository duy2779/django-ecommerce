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

@method_decorator(staff_member_required, name='dispatch')
class Menus(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        menus = Menu.objects.exclude(status=0)
        categories = Category.objects.filter(status=1)
        topics = Topic.objects.filter(status=1)
        pages = Post.objects.filter(status=1, type='page')
        context = {'menus':menus, 'categories':categories, 'topics':topics, 'pages':pages}
        return render(request, 'admin/menu/index.html', context)

    def post(self, request):
        count = 0
        if 'add-cat' in request.POST:
            items = request.POST.getlist('itemCat')
            for item in items:
                cat = Category.objects.get(id=item)
                Menu.objects.create(name=cat.name, link=cat.slug, type='category', status=2, updated_by=request.user, category=cat)
                count+=1
            messages.success(request,'Thêm "'+str(count)+'" menu thành công')
            return redirect('admin:menus')
        elif 'add-top' in request.POST:
            items = request.POST.getlist('itemTop')
            for item in items:
                top = Topic.objects.get(id=item)
                Menu.objects.create(name=top.name, link=top.slug, type='topic', status=2, updated_by=request.user, topic=top)
                count+=1
            messages.success(request,'Thêm "'+str(count)+'" menu thành công')
            return redirect('admin:menus')
        elif 'add-page' in request.POST:
            items = request.POST.getlist('itemPage')
            for item in items:
                page = Post.objects.get(id=item)
                Menu.objects.create(name=page.title, link=page.slug, type='page', status=2, updated_by=request.user, post=page)
                count+=1
            messages.success(request,'Thêm "'+str(count)+'" menu thành công')
            return redirect('admin:menus')
        else:
            name = request.POST.get('name')
            link = request.POST.get('link')
            Menu.objects.create(name=name, link=link, type='custom', status=2, updated_by=request.user)
            messages.success(request,'Thêm "'+str(count)+'" menu thành công')
            return redirect('admin:menus')

@staff_member_required(login_url='admin:login')
def menus_trash(request):
    menus = Menu.objects.filter(status=0)
    context = {'menus':menus}
    return render(request, 'admin/menu/trash.html' , context)

@staff_member_required(login_url='admin:login')
def menu_status(request, id):
    try:
        menu = Menu.objects.get(id=id)
        if menu.status == 1:
            menu.status = 2
        else:
            menu.status = 1
        menu.save()
        messages.success(request,'Thay đổi trạng thái thành công')
    except:
        messages.error(request,'Menu không tồn tại')
    return redirect('admin:menus')

@staff_member_required(login_url='admin:login')
def menu_deltrash(request, id):
    try:
        menu = Menu.objects.get(id=id)
        menu.status = 0
        menu.save()
        messages.success(request,'Xóa vào thùng rác thành công')
    except:
        messages.error(request,'Menu tồn tại')
    return redirect('admin:menus')

@staff_member_required(login_url='admin:login')
def menu_retrash(request, id):
    try:
        menu = Menu.objects.get(id=id)
        menu.status = 2
        menu.save()
        messages.success(request,'Khôi phục thành công')
    except:
        messages.error(request,'Nenu không tồn tại')
    return redirect('admin:menus_trash')

@method_decorator(staff_member_required, name='dispatch')
class MenuDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
        except:
            messages.error(request,'Menu không tồn tại')
            return redirect('admin:menus_trash')
        context = {'menu':menu}
        return render(request, 'admin/menu/delete.html', context)

    def post(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
        except:
            messages.error(request,'Menu không tồn tại')
            return redirect('admin:menus_trash')
        menu.delete()
        messages.success(request,'Xóa "'+menu.name+'" thành công')
        return redirect('admin:menus_trash')


@method_decorator(staff_member_required, name='dispatch')
class MenuUpdate(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
        except:
            messages.error(request,'Menu không tồn tại')
            return redirect('admin:menus')
        try:
            order = Menu.objects.get(order=menu.order-1)#exist parent
        except:
            order = {}
        menus = Menu.objects.filter(status=1).exclude(id=menu.id)
        context = {'menus':menus, 'menu':menu, 'order':order}
        return render(request, 'admin/menu/edit.html', context)

    def post(self, request, id):
        menu = Menu.objects.get(id=id)
        name = request.POST.get('name')
        parent_id = request.POST.get('parent-id')
        if parent_id =='':
            parent = None
        else:
            parent = Menu.objects.get(id=parent_id)
        if int(request.POST.get('order')) == menu.order:
            order = int(request.POST.get('order'))
        elif int(request.POST.get('order')) == 0:
            order = 0
        else:
            order = int(request.POST.get('order')) + 1
        status = request.POST.get('status')
        if menu.type == 'custom':
            link= request.POST.get('link')
        else:
            link = slugify(name)
        user = request.user
        menu.name = name
        menu.parent_id = parent
        menu.order = order
        menu.link = link
        menu.status = status
        menu.created_by = user
        menu.updated_by = user
        menu.save()
        messages.success(request,'Cập nhật"'+name+'" thành công')
        return redirect('admin:menus')