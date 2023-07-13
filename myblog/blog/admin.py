from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'author',
        'body',
        'publish',
        'status',
    )
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    list_filter = ('author', 'status', 'created', 'publish')
    empty_value_display = '--пусто--'
