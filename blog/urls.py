from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.all_post, name='all_post'),
    path('<str:top>/', views.topic_view, name='topic_view'),
    path('<str:top>/<str:post>/', views.post_view, name='post_view'),
]