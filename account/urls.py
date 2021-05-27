from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.index, name='index'),
    path('dang-ki', views.register, name='register'),
    path('dang-nhap', views.sign_in, name='sign_in'),
    path('dang-xuat', views.logoutUser, name='logout'),
    path('don-hang', views.order, name='order'),
    path('don-hang/huy/<int:id>', views.OrderCancel.as_view(), name='order_cancel'),
    path('don-hang/chi-tiet/<int:id>', views.order_item, name='order_item'),
]