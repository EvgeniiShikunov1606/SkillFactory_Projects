from celery import shared_task
import time
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta


@shared_task
def send_weekly_newsletter():
    from news.models import Post, Category
    today = now().date()
    last_week = today - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__date__gte=last_week)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            category_posts = recent_posts.filter(categories=category)
            if category_posts.exists():
                subject = f'Еженедельная подборка новостей для категории: {category.name}'
                message = (
                    f'Здравствуйте! Вот последние новости из категории "{category.name}":\n\n' +
                    '\n\n'.join(
                        f'{post.title} - {post.get_absolute_url()}' for post in category_posts
                    ) +
                    '\n\nСпасибо, что остаётесь с нами!'
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='evgeniishikunov1998@ya.ru',
                    recipient_list=[subscriber.email for subscriber in subscribers],
                )


@shared_task
def send_post_notification(post_id):
    from news.models import Post
    try:
        post = Post.objects.get(id=post_id)
        categories = post.categories.all()
        subscribers = set(user.email for category in categories for user in category.subscribers.all())

        if subscribers:
            subject = f'Новая публикация: {post.title}'
            message = (
                f'Заголовок: {post.title}\n'
                f'Категории: {", ".join(cat.name for cat in categories)}\n\n'
                f'Содержание:\n{post.text}\n\n'
                f'Ссылка: http://127.0.0.1:8000{post.get_absolute_url()}'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email='evgeniishikunov1998@ya.ru',
                recipient_list=subscribers,
            )
    except Post.DoesNotExist:
        print(f'Пост с ID {post_id} не существует')


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

