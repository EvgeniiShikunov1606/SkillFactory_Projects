from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ("tanks", "Танки"),
    ("healers", "Хилы"),
    ("dd", "ДД"),
    ("traders", "Торговцы"),
    ("guildmasters", "Гилдмастеры"),
    ("questgivers", "Квестгиверы"),
    ("blacksmiths", "Кузнецы"),
    ("leatherworkers", "Кожевники"),
    ("alchemists", "Зельевары"),
    ("spellmasters", "Мастера заклинаний"),
]


class Ad(models.Model):
    title = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to="ads_images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="ads_images/", blank=True, null=True)
    video1 = models.FileField(upload_to="ads_videos/", blank=True, null=True)
    video2 = models.FileField(upload_to="ads_videos/", blank=True, null=True)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="responses")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик от {self.author.username} на '{self.ad.title}'"


class AdsLetter(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Текст письма")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
