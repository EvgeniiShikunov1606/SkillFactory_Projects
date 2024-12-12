from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.core.exceptions import ValidationError
from .models import Category, Post
from django.db.models.signals import pre_save
from django.utils.timezone import now
from .tasks import send_post_notification


@receiver(post_save, sender=Category)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'subject text (if)'
    else:
        subject = f'subject test (else)'

    mail_managers(
        subject=subject,
        message=instance.message,
    )


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    if instance.pk is None:
        today = now().date()
        posts_today = Post.objects.filter(author=instance.author, created_at__date=today).count()
        if posts_today >= 5:
            raise ValidationError("Вы не можете публиковать более пяти новостей в день.")


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        # Убедимся, что связанные данные сохранены
        instance.refresh_from_db()
        send_post_notification.delay(instance.id)

