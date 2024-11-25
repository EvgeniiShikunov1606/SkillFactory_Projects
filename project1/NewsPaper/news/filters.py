from django_filters import FilterSet, DateTimeFilter, DateFilter, CharFilter
from django.forms.widgets import DateInput
from datetime import datetime, timedelta
from .models import Post


class PostFilter(FilterSet):
    created_at__lte = DateTimeFilter(
        field_name='created_at', method='filter_lte_with_end_of_day', label='По дату',
        widget=DateInput(attrs={'type': 'date'})
    )
    author = CharFilter(
        field_name='author__user__username', lookup_expr='icontains', label='Автор'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['exact'],
            'text': ['icontains', 'exact'],
        }

    def filter_lte_with_end_of_day(self, queryset, name, value):
        if value:
            end_of_day = datetime.combine(value, datetime.max.time())
            return queryset.filter(**{f"{name}__lte": end_of_day})
        return queryset
