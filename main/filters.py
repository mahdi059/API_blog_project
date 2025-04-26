import django_filters
from .models import Blog
from django.contrib.auth.models import User


class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    created_at = django_filters.DateFromToRangeFilter(label='Created at')
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Author')
    private_blog = django_filters.BooleanFilter(label='Private blog')

    class Meta:
        model = Blog
        fields = ['title', 'created_at', 'user', 'private_blog']
