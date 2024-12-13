from celery import shared_task
import time
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Post, Category
from django.core.mail import EmailMessage


@shared_task(bind=True)
def send_post_notification(self, post_id):
    try:
        post = Post.objects.select_related('author').prefetch_related('categories').get(id=post_id)
        categories = post.categories.all()
        subscribers = set(user.email for category in categories for user in category.subscribers.all())
        subject = f'Новая публикация: {post.title}'
        message = (
            f'Заголовок: {post.title}\n'
            f'Категории: {", ".join(cat.name for cat in categories)}\n\n'
            f'Содержание:\n{post.text}\n\n'
        )

        for email in subscribers:
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email='evgeniishikunov1998@ya.ru',
                to=[email],
            )
            email_message.send()

        print(f'Письма успешно отправлены. ID поста: {post_id}')
        return 'Успешно отправлено'
    except Post.DoesNotExist:
        print(f'Пост с ID {post_id} не найден.')
        self.retry(exc=Exception('Пост не найден'), countdown=5, max_retries=3)
    except Exception as e:
        print(f'Ошибка при выполнении задачи: {e}')
        self.retry(exc=e, countdown=5, max_retries=3)


@shared_task
def send_weekly_newsletter():
    today = now().date()
    last_week = today - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=last_week)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            category_posts = recent_posts.filter(categories__in=[category])
            if category_posts.exists():
                subject = f'Еженедельная подборка новостей для категории: {category.name}'
                posts_text = "\n".join(
                    f'{post.title} - {post.text}' for post in category_posts
                )
                message = (
                    f'Здравствуйте! Вот последние новости из категории "{category.name}":\n\n'
                    f'{posts_text}\n\n'
                    'С уважением, ваша команда NewsPaper.'
                )
                recipient_list = [subscriber.email for subscriber in subscribers]
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='evgeniishikunov1998@ya.ru',
                    recipient_list=recipient_list,
                )
