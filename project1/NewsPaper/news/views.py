from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    posting = 'title'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
