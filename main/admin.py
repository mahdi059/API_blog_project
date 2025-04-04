from django.contrib import admin
from .models import Blog, BlogAccess, Comment, Favorite

admin.site.register(Blog)
admin.site.register(BlogAccess)
admin.site.register(Comment)
admin.site.register(Favorite)