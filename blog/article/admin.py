from django.contrib import admin

# Register your models here.

# 别忘了导入ArticlePost
from .models import ArticlePost

# 注册ArticlePost到admin
admin.site.register(ArticlePost)
