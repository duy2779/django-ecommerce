from django.shortcuts import render
from store.models import Category, Product, Menu
from django.http import HttpResponse

# Create your views he


def all_product(request):
    all_product = Product.objects.filter(status=1).order_by('created_at')
    categories = Category.objects.filter(parent_id__isnull=True)
    total = Product.objects.filter(status=1).count()
    context = {'title':'Tất cả sản phẩm', 'products':all_product, 'categories':categories, 'total':total}
    return render(request, 'store/shop.html', context)


def category_view(request, cat):
    if not Category.objects.filter(slug=cat):
        return HttpResponse("Nothing here")
    else:
        categories = Category.objects.filter(parent_id__isnull=True)
        id=Category.objects.values_list('id', flat=True).get(slug=cat)
        total = Product.objects.filter(category__slug=cat, status=1).count() | Product.objects.filter(category__parent_id=id, status=1).count()
        parent_id= Category.objects.values_list('parent_id', flat=True).filter(parent_id=id)
        category_product = Product.objects.filter(category__slug=cat, status=1).order_by('created_at') | Product.objects.filter(category__parent_id=id, status=1).order_by('created_at')
        name = Category.objects.values_list('name', flat=True).get(slug=cat)
        context = {'title':name, 'products':category_product, 'categories':categories, 'total':total}
        return render(request, 'store/shop.html', context)


def product_view(request, cat, product):
    product_detail = Product.objects.get(slug=product)
    related_product = Product.objects.exclude(slug=product).filter(category__slug=cat).order_by('created_at')
    context={'products':product_detail, 'related_product':related_product}
    return render(request, 'store/product.html', context)
