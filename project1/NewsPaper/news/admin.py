from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post)
