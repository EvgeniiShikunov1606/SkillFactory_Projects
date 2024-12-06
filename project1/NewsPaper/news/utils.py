from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def notify_subscribers(post):
    categories = post.categories.all()
    subscribers = set()

    for category in categories:
        subscribers.update(category.subscribers.all())

    for user in subscribers:
        subject = post.title
        html_content = render_to_string(
            'email_notification.html',
            {
                'user': user,
                'post': post,
            }
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
            from_email='evgeniishikunov1998@ya.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
