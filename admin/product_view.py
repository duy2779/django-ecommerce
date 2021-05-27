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
def products(request):
    products = Product.objects.exclude(status=0).order_by('-created_at')
    context = {'products': products}
    return render(request, 'admin/product/index.html', context)


@staff_member_required(login_url='admin:login')
def products_trash(request):
    products = Product.objects.filter(status=0).order_by('-created_at')
    context = {'products': products}
    return render(request, 'admin/product/trash.html', context)


@staff_member_required(login_url='admin:login')
def product_status(request, id):
    try:
        product = Product.objects.get(id=id)
        if product.status == 1:
            product.status = 2
        else:
            product.status = 1
        product.save()
        messages.success(request,'Thay đổi trạng thái thành công')
    except:
        messages.error(request,'Sản phẩm không tồn tại')
    return redirect('admin:products')


@staff_member_required(login_url='admin:login')
def product_deltrash(request, id):
    try:
        product = Product.objects.get(id=id)
        product.status = 0
        product.save()
        messages.success(request,'Xóa vào thùng rác thành công')
    except:
        messages.error(request,'Sản phẩm không tồn tại')
    return redirect('admin:products')


@staff_member_required(login_url='admin:login')
def product_retrash(request, id):
    try:
        product = Product.objects.get(id=id)
        product.status = 2
        product.save()
        messages.success(request,'Khôi phục thành công')
    except:
        messages.error(request,'Sản phẩm không tồn tại')
    return redirect('admin:products_trash')


@method_decorator(staff_member_required, name='dispatch')
class ProductAdd(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        categories = Category.objects.filter(status=1)
        context = {'categories':categories}
        return render(request, 'admin/product/add.html', context)

    def post(self, request):
        name = request.POST.get('name')
        cat_id = request.POST.get('category')
        category = Category.objects.get(id=cat_id)
        number = request.POST.get('number')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        price = request.POST.get('price')
        price_sale = request.POST.get('price-sale')
        if not price_sale:
            price_sale = None
        featured = request.POST.get('featured')
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if Product.objects.filter(slug=slug).count() > 0:
            messages.error(request,'Tên sản phẩm đã tồn tại')
            return redirect('admin:product_add')
        else:
            try:
                upload_file = request.FILES['image']
                fs = FileSystemStorage()
                fs.save(upload_file.name, upload_file)
                img= upload_file.name
            except:
                img = None
            Product.objects.create(name=name, category=category, slug=slug, number=number, img=img, description=description, detail=detail, price=price, price_sale=price_sale, featured=featured, created_by=user, updated_by=user, status=status)
            #save image
            messages.success(request,'Thêm "'+name+'" thành công')
            return redirect('admin:products')

@method_decorator(staff_member_required, name='dispatch')
class ProductUpdate(LoginRequiredMixin,View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except:
            messages.error(request,'Sản phẩm không tồn tại')
            return redirect('admin:categories')
            order = {}
        categories = Category.objects.filter(status=1).exclude(id=product.category.id)
        context = {'product': product, 'categories':categories}
        return render(request, 'admin/product/edit.html', context)

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        name = request.POST.get('name')
        cat_id = request.POST.get('category')
        category = Category.objects.get(id=cat_id)
        number = request.POST.get('number')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        price = request.POST.get('price')
        price_sale = request.POST.get('price-sale')
        if not price_sale:
            price_sale = None
        featured = request.POST.get('featured')
        status = request.POST.get('status')
        slug = slugify(name)
        user = request.user
        if name != product.name:
            if Product.objects.filter(slug=slug).count() > 0:
                messages.error(request,'Tên sản phẩm đã tồn tại')
                return redirect('admin:product_update', slug=product.slug)
            else:
                product.name = name
        try:
            upload_file = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(upload_file.name, upload_file)
            product.img.delete()
            product.img = upload_file.name
        except:
            pass
        product.number = number
        product.description = description
        product.price = price
        product.price_sale = price_sale
        product.category = category
        product.detail = detail
        product.featured = featured
        product.slug = slug
        product.status = status
        product.created_by = user
        product.updated_by = user
        product.save()
        messages.success(request,'Cập nhật"'+name+'" thành công')
        return redirect('admin:products')


@method_decorator(staff_member_required, name='dispatch')
class ProductDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except:
            messages.error(request,'Sản phẩm không tồn tại')
            return redirect('admin:products_trash')
        context = {'product':product}
        return render(request, 'admin/product/delete.html', context)

    def post(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except:
            messages.error(request,'Loại sản phẩm không tồn tại')
            return redirect('admin:products_trash')
        product.delete()
        messages.success(request,'Xóa "'+product.name+'" thành công')
        return redirect('admin:products_trash')