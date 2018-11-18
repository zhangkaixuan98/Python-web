from django.contrib import admin
from django.db import models
from . import models


class userAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_id','user_url')


admin.site.register(models.user, userAdmin)


class blogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_id', 'blog_date_time')


admin.site.register(models.blog, blogAdmin)
