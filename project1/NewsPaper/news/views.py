from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    posting = 'title'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
