from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.all_product, name='all_product'),
    path('<str:cat>/', views.category_view, name='category_view'),
    path('<str:cat>/<str:product>/', views.product_view, name='product_view'),
]