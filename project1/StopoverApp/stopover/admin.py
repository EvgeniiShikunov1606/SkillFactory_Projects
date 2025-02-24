from django.contrib import admin
from .models import User, Stopover, StopoverImage


admin.site.register(User)
admin.site.register(Stopover)
admin.site.register(StopoverImage)
