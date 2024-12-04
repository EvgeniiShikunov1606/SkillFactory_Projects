from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView


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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='authors').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        author, created = Author.objects.get_or_create(user=user)
        form.instance.author = author
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author.user != request.user or not request.user.groups.filter(name='authors').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class SearchPostsView(ListView):
    model = Post
    template_name = 'flatpages/search_posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
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


@login_required
def profile_view(request):
    is_author = request.user.groups.filter(name='authors').exists()
    context = {
        'is_not_authors': not is_author,
        'is_author': is_author,
    }
    return render(request, 'flatpages/profile.html', context)

