from django.contrib import admin
from .models import Post
@admin.register(Post) #将postAdmin 类注册成post的管理类
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status',)
    list_filter = ('status','created','publish','author',)
    search_fields = ('title','body',)
    #根据标题自动填写SLUG
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','publish')
# Register your models here.
