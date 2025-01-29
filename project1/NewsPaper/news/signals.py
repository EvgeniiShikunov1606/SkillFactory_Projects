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
    subject = 'subject text (if)' if created else 'subject text (else)'

    # Предположим, у вас есть поле 'name' в модели Category
    message = f'The category "{instance.name}" has been {"created" if created else "updated"}.'

    mail_managers(
        subject=subject,
        message=message,
    )


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    if instance.pk is None:
        today = now().date()
        posts_today = Post.objects.filter(author=instance.author, created_at__date=today).count()
        if posts_today >= 20:
            raise ValidationError("Вы не можете публиковать более двадцати постов в день.")


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_post_notification.delay(instance.id)

