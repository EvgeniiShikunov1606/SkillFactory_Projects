from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['exact'],
            'text': ['icontains', 'exact'],
            'created_at': ['gte', 'lte']
        }
