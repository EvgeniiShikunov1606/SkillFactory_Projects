from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

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
    name = models.CharField(max_length=50, unique=True)
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
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=ARTICLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
