from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_('author'))
    rating = models.IntegerField(default=0, help_text=_('rating'))

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        post_rating = sum(post.rating * 3 for post in self.post_set.all())
        comment_rating = sum(
            comment.rating
            for comment in Comment.objects.filter(user_id=self.user)
        )

        comment_post_rating = sum(
            comment.rating
            for comment in Comment.objects.filter(post__author=self)
        )
        self.rating = post_rating + comment_rating + comment_post_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text=_('category name'))
    subscribers = models.ManyToManyField(
        User,
        related_name='subscribed_categories'
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPE_CHOICES = (
        (ARTICLE, _('Статья')),
        (NEWS, _('Новость')),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text=_('author'))
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=ARTICLE,
        help_text=_('type')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, help_text=_('title'))
    text = models.TextField(help_text=_('text'))
    rating = models.IntegerField(default=0, help_text=_('rating'))

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('help text for post (model PostCategory)', 'The post text'))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('help text for category (model PostCategory)', 'This is the help text'),)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
