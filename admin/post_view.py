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
from django.core.files.storage import FileSystemStorage

@staff_member_required(login_url='admin:login')
def posts(request):
    posts = Post.objects.exclude(status=0).order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'admin/post/index.html', context)


@staff_member_required(login_url='admin:login')
def posts_trash(request):
    posts = Post.objects.filter(status=0).order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'admin/post/trash.html', context)

@staff_member_required(login_url='admin:login')
def post_status(request, id):
    try:
        post = Post.objects.get(id=id)
        if post.status == 1:
            post.status = 2
        else:
            post.status = 1
        post.save()
        messages.success(request,'Thay đổi trạng thái thành công')
    except:
        messages.error(request,'Bài viết không tồn tại')
    return redirect('admin:posts')


@staff_member_required(login_url='admin:login')
def post_deltrash(request, id):
    try:
        post = Post.objects.get(id=id)
        post.status = 0
        post.save()
        messages.success(request,'Xóa vào thùng rác thành công')
    except:
        messages.error(request,'Bài viết không tồn tại')
    return redirect('admin:posts')


@staff_member_required(login_url='admin:login')
def post_retrash(request, id):
    try:
        post = Post.objects.get(id=id)
        post.status = 2
        post.save()
        messages.success(request,'Khôi phục thành công')
    except:
        messages.error(request,'Bài viết không tồn tại')
    return redirect('admin:posts_trash')


@method_decorator(staff_member_required, name='dispatch')
class PostDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except:
            messages.error(request,'Bài viết không tồn tại')
            return redirect('admin:posts_trash')
        context = {'post':post}
        return render(request, 'admin/post/delete.html', context)

    def post(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except:
            messages.error(request,'Bài viết không tồn tại')
            return redirect('admin:posts_trash')
        post.delete()
        messages.success(request,'Xóa "'+post.title+'" thành công')
        return redirect('admin:posts_trash')

@method_decorator(staff_member_required, name='dispatch')
class PostAdd(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        topics = Topic.objects.filter(status=1)
        context = {'topics':topics}
        return render(request, 'admin/post/add.html', context)

    def post(self, request):
        title = request.POST.get('title')
        top_id = request.POST.get('topic')
        topic = Topic.objects.get(id=top_id)
        detail = request.POST.get('detail')
        type = request.POST.get('type')
        if type == 'page':
            topic = None
        status = request.POST.get('status')
        slug = slugify(title)
        user = request.user
        if Post.objects.filter(slug=slug).count() > 0:
            messages.error(request,'Tên bài viết đã tồn tại')
            return redirect('admin:post_add')
        else:
            try:
                upload_file = request.FILES['image']
                fs = FileSystemStorage()
                fs.save(upload_file.name, upload_file)
                img= upload_file.name
            except:
                img = None
            Post.objects.create(title=title, topic=topic, slug=slug, img=img, detail=detail, type=type, created_by=user, updated_by=user, status=status)
            #save image
            messages.success(request,'Thêm "'+title+'" thành công')
            return redirect('admin:posts')

@method_decorator(staff_member_required, name='dispatch')
class PostUpdate(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except:
            messages.error(request,'Bài viết không tồn tại')
            return redirect('admin:posts')
        topics = {}
        if post.type == 'post':
            topics = Topic.objects.filter(status=1).exclude(id=post.topic.id)
        context = {'post': post, 'topics':topics}
        return render(request, 'admin/post/edit.html', context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        title = request.POST.get('title')
        if post.type == 'post':
            top_id = request.POST.get('topic')
            topic = Topic.objects.get(id=top_id)
            post.topic = topic
        detail = request.POST.get('detail')
        status = request.POST.get('status')
        slug = slugify(title)
        user = request.user
        if title != post.title:
            if Post.objects.filter(slug=slug).count() > 0:
                messages.error(request,'Tên bài viết đã tồn tại')
                return redirect('admin:post_update', slug=post.slug)
            else:
                post.title = title
        try:
            upload_file = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(upload_file.name, upload_file)
            post.img.delete()
            post.img = upload_file.name
        except:
            pass
        post.detail = detail
        post.slug = slug
        post.status = status
        post.created_by = user
        post.updated_by = user
        post.save()
        messages.success(request,'Cập nhật"'+title+'" thành công')
        return redirect('admin:posts')