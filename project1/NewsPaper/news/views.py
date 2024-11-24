from datetime import datetime
from django.views.generic import ListView, DetailView

from .filters import PostFilter
from .models import Post


class PostsList(ListView):
    model = Post
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3
    filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['total_posts'] = Post.objects.count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
