from django.shortcuts import render
from store.models import Topic, Post
from django.http import HttpResponse

# Create your views here.

def all_post(request):
    all_post = Post.objects.filter(topic__isnull=False).order_by('created_at')
    context = {'title':'Tất cả bài viết', 'posts':all_post}
    return render(request, 'store/blog.html', context)


def topic_view(request, top):
    if not Topic.objects.filter(slug=top):
        return HttpResponse("Nothing here")
    else:
        id=Topic.objects.values_list('id', flat=True).get(slug=top)
        parent_id= Topic.objects.values_list('parent_id', flat=True).filter(parent_id=id)
        topic_post = Post.objects.filter(topic__slug=top).order_by('created_at') | Post.objects.filter(topic__parent_id=id).order_by('created_at')
        name = Topic.objects.values_list('name', flat=True).get(slug=top)
        context = {'title':name, 'posts':topic_post}
        return render(request, 'store/blog.html', context)


def post_view(request, top, post):
    post_detail = Post.objects.get(slug=post)
    related_post = Post.objects.exclude(slug=post).filter(topic__slug=top).order_by('created_at')[:3]
    context={'post':post_detail, 'related_post':related_post}
    return render(request, 'store/blog_single.html', context)