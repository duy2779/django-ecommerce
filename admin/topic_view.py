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
def topics(request):
    topics = Topic.objects.exclude(status=0)
    context = {'topics':topics}
    return render(request, 'admin/topic/index.html' , context)

@staff_member_required(login_url='admin:login')
def topics_trash(request):
    topics = Topic.objects.filter(status=0)
    context = {'topics':topics}
    return render(request, 'admin/topic/trash.html' , context)

@staff_member_required(login_url='admin:login')
def topic_status(request, id):
    try:
        topic = Topic.objects.get(id=id)
        if topic.status == 1:
            topic.status = 2
        else:
            topic.status = 1
        topic.save()
        messages.success(request,'Thay đổi trạng thái thành công')
    except:
        messages.error(request,'Chủ đề không tồn tại')
    return redirect('admin:topics')

@staff_member_required(login_url='admin:login')
def topic_deltrash(request, id):
    try:
        topic = Topic.objects.get(id=id)
        topic.status = 0
        topic.save()
        messages.success(request,'Xóa vào thùng rác thành công')
    except:
        messages.error(request,'Chủ đề không tồn tại')
    return redirect('admin:topics')

@staff_member_required(login_url='admin:login')
def topic_retrash(request, id):
    try:
        topic = Topic.objects.get(id=id)
        topic.status = 2
        topic.save()
        messages.success(request,'Khôi phục thành công')
    except:
        messages.error(request,'Chủ đề không tồn tại')
    return redirect('admin:topics_trash')

@method_decorator(staff_member_required, name='dispatch')
class TopicAdd(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        topics = Topic.objects.filter(status=1)
        context = {'topics':topics}
        return render(request, 'admin/topic/add.html', context)

    def post(self, request):
        name = request.POST.get('name')
        parent_id = request.POST.get('parent-id')
        if parent_id =='':
            parent = None
        else:
            parent = Topic.objects.get(id=parent_id)
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if Topic.objects.filter(slug=slug).count() > 0:
            messages.error(request,'Tên chủ đề đã tồn tại')
            return redirect('admin:topic_add')
        else:
            Topic.objects.create(name=name, parent_id=parent, slug=slug, created_by=user, updated_by=user, status=status)
            messages.success(request,'Thêm "'+name+'" thành công')
            return redirect('admin:topics')


@method_decorator(staff_member_required, name='dispatch')
class TopicUpdate(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            topic = Topic.objects.get(slug=slug)
        except:
            messages.error(request,'Chủ đề không tồn tại')
            return redirect('admin:topics')
        topics = Topic.objects.filter(status=1).exclude(id=topic.id)
        context = {'topics':topics, 'topic':topic}
        return render(request, 'admin/topic/edit.html', context)

    def post(self, request, slug):
        topic = Topic.objects.get(slug=slug)
        name = request.POST.get('name')
        parent_id = request.POST.get('parent-id')
        if parent_id =='':
            parent = None
        else:
            parent = Topic.objects.get(id=parent_id)
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if name != topic.name:
            if Topic.objects.filter(slug=slug).count() > 0:
                messages.error(request,'Tên chủ đề đã tồn tại')
                return redirect('admin:topic_update', slug=topic.slug)
            else:
                topic.name = name
        topic.parent_id = parent
        topic.slug = slug
        topic.status = status
        topic.created_by = user
        topic.updated_by = user
        topic.save()
        messages.success(request,'Cập nhật"'+name+'" thành công')
        return redirect('admin:topics')

@method_decorator(staff_member_required, name='dispatch')
class TopicDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            topic = Topic.objects.get(slug=slug)
        except:
            messages.error(request,'Chủ đề không tồn tại')
            return redirect('admin:topics_trash')
        context = {'topic':topic}
        return render(request, 'admin/topic/delete.html', context)

    def post(self, request, slug):
        try:
            topic = Topic.objects.get(slug=slug)
        except:
            messages.error(request,'Chủ đề không tồn tại')
            return redirect('admin:topics_trash')
        topic.delete()
        messages.success(request,'Xóa "'+topic.name+'" thành công')
        return redirect('admin:topics_trash')