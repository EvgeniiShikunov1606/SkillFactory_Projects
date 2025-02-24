from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.fam}{f' {self.otc}' if self.otc else ''}"


class StopoverLevel(models.Model):
    level_winter = models.CharField(max_length=10, blank=True, null=True)
    level_summer = models.CharField(max_length=10, blank=True, null=True)
    level_autumn = models.CharField(max_length=10, blank=True, null=True)
    level_spring = models.CharField(max_length=10, blank=True, null=True)


class StopoverCoords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.PositiveIntegerField()


class Stopover(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.TextField(blank=True, null=True)
    connect = models.TextField(blank=True, null=True)

    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='stopover', on_delete=models.CASCADE)

    coords = models.ForeignKey(
        StopoverCoords,
        related_name='stopover_coords',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    level = models.ForeignKey(StopoverLevel, related_name='stopover_level', on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.title} ({self.status})"


class StopoverImage(models.Model):
    stopover = models.ForeignKey(Stopover, related_name='images', on_delete=models.CASCADE)
    data = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.stopover.title})"
