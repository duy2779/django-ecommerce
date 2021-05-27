from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('san-pham/',include('shop.urls')),
    path('bai-viet/',include('blog.urls')),
    path('tai-khoan/',include('account.urls')),
    path('lien-he/', views.Contact.as_view(), name='contact'),
    path('gio-hang/', views.cart, name='cart'),
    path('update_item/', views.update_item, name='update_item'),
    path('thanh-toan/', views.checkout, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
    path('product/', views.product, name='product'),
    path('deal/', views.deal, name='deal'),
    path('<str:slug>/', views.page_view, name='page_view'),
]