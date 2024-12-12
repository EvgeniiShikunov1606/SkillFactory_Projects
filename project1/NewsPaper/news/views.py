from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import render, reverse, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .tasks import send_post_notification, send_weekly_newsletter


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
        context['categories'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'flatpages/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Все категории
        return context


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

    def send_email_notification(self):
        post = self.object
        user = self.request.user

        if not user.email:
            return

        html_content = render_to_string(
            'email_notification.html',
            {
                'post': post,
                'user': user,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"Новый пост: {post.title}",
            body=f"Вы только что создали новый пост: {post.title}",
            from_email='evgeniishikunov1998@ya.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


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


@login_required
def subscribe_to_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.user in category.subscribers.all():
        messages.info(request, 'Вы уже подписаны на эту категорию.')
    else:
        category.subscribers.add(request.user)
        messages.success(request, f'Вы успешно подписались на категорию {category.name}.')
    return redirect('category_detail', pk=category.id)


class TaskView(View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        send_post_notification.delay(post_id)
        return HttpResponse('Задача отправлена в очередь')
