from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import BlogCategory, Blog, BlogComment

class BlogAdmin(ModelAdmin):
    list_display = ['id', 'category', 'title', 'time']

class BlogCommentAdmin(ModelAdmin):
    list_display = ['id', 'author', 'content', 'blog']

class BlogCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name']

# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)