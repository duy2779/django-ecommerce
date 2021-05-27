from django.urls import path
from . import views
from . import category_view
from . import product_view
from . import post_view
from . import order_view
from . import topic_view
from . import menu_view
from . import contact_view
from . import customer_view
from . import staff_view

app_name = "admin"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dang-nhap/', views.sign_in, name='login'),
    path('dang-xuat/', views.logoutUser, name='logout'),

    path('category/', category_view.categories, name='categories'),
    path('category/status/<int:id>/', category_view.category_status, name='category_status'),
    path('category/deltrash/<int:id>/', category_view.category_deltrash, name='category_deltrash'),
    path('category/retrash/<int:id>/', category_view.category_retrash, name='category_retrash'),
    path('category/add/', category_view.CategoryAdd.as_view(), name='category_add'),
    path('category/update/<str:slug>/', category_view.CategoryUpdate.as_view(), name='category_update'),
    path('category/trash/', category_view.categories_trash, name='categories_trash'),
    path('category/delete/<str:slug>/', category_view.CategoryDelete.as_view(), name='category_delete'),

    path('topic/', topic_view.topics, name='topics'),
    path('topic/status/<int:id>/', topic_view.topic_status, name='topic_status'),
    path('topic/deltrash/<int:id>/', topic_view.topic_deltrash, name='topic_deltrash'),
    path('topic/retrash/<int:id>/', topic_view.topic_retrash, name='topic_retrash'),
    path('topic/add/', topic_view.TopicAdd.as_view(), name='topic_add'),
    path('topic/update/<str:slug>/', topic_view.TopicUpdate.as_view(), name='topic_update'),
    path('topic/trash/', topic_view.topics_trash, name='topics_trash'),
    path('topic/delete/<str:slug>/', topic_view.TopicDelete.as_view(), name='topic_delete'),

    path('menu/', menu_view.Menus.as_view(), name='menus'),
    path('menu/status/<int:id>/', menu_view.menu_status, name='menu_status'),
    path('menu/deltrash/<int:id>/', menu_view.menu_deltrash, name='menu_deltrash'),
    path('menu/retrash/<int:id>/', menu_view.menu_retrash, name='menu_retrash'),
    path('menu/trash/', menu_view.menus_trash, name='menus_trash'),
    path('menu/delete/<int:id>/', menu_view.MenuDelete.as_view(), name='menu_delete'),
    path('menu/update/<int:id>/', menu_view.MenuUpdate.as_view(), name='menu_update'),

    path('product/', product_view.products, name='products'),
    path('product/trash/', product_view.products_trash, name='products_trash'),
    path('product/status/<int:id>/', product_view.product_status, name='product_status'),
    path('product/deltrash/<int:id>/', product_view.product_deltrash, name='product_deltrash'),
    path('product/retrash/<int:id>/', product_view.product_retrash, name='product_retrash'),
    path('product/add/', product_view.ProductAdd.as_view(), name='product_add'),
    path('product/update/<str:slug>/', product_view.ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<str:slug>/', product_view.ProductDelete.as_view(), name='product_delete'),

    path('post/', post_view.posts, name='posts'),
    path('post/trash/', post_view.posts_trash, name='posts_trash'),
    path('post/status/<int:id>/', post_view.post_status, name='post_status'),
    path('post/deltrash/<int:id>/', post_view.post_deltrash, name='post_deltrash'),
    path('post/retrash/<int:id>/', post_view.post_retrash, name='post_retrash'),
    path('post/add/', post_view.PostAdd.as_view(), name='post_add'),
    path('post/update/<str:slug>/', post_view.PostUpdate.as_view(), name='post_update'),
    path('post/delete/<str:slug>/', post_view.PostDelete.as_view(), name='post_delete'),

    path('order/', order_view.orders, name='orders'),
    path('order/complete', order_view.orders_complete, name='orders_complete'),
    path('order/status/<int:id>/', order_view.order_status, name='order_status'),
    path('order/detail/<int:id>/', order_view.order_detail, name='order_detail'),

    path('contact/', contact_view.contacts, name='contacts'),
    path('contact/delete/<int:id>/', contact_view.ContactDelete.as_view(), name='contact_delete'),

    path('customer/', customer_view.customers, name='customers'),

    path('staff/', staff_view.staffs, name='staffs'),
    path('staff/add', staff_view.StaffAdd.as_view(), name='staff_add'),
    path('staff/delete/<int:id>/', staff_view.StaffDelete.as_view(), name='staff_delete'),
]