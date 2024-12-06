from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'type', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if title is not None and len(title) < 10:
            raise ValidationError({
                "title": "Содержимое не может быть менее 10 символов."
            })
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Содержимое не может быть менее 20 символов."
            })
        if title == text:
            raise ValidationError({
                "title": "Заголовок не должен быть идентичным содержимому."
            })

        return cleaned_data


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []
