from django.contrib import admin

from .models import *



# Register Post model.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'publish')
    list_filter = ('status',)
    search_fields = ('title', 'slug', 'author')
    date_hierarchy = 'publish'
    list_editable = ('status',)
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'active', 'create')
    list_filter = ('create',)
    search_fields = ('post', 'name', 'active')
    
    