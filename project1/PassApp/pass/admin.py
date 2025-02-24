from django.contrib import admin
from .models import User, Pass, PassImage


admin.site.register(User)
admin.site.register(Pass)
admin.site.register(PassImage)
