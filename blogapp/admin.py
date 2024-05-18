from django.contrib import admin
from  .models import Category, Post, Tag, Imajes
# Register your models here.

admin.site.register(Category)


def clear_rating(modeladmin, request, queryset):
    queryset.update(rating=1)


clear_rating.short_description = "Выставить рейтинг = 1"

def set_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text', 'category', 'display_tags', 'has_image', 'rating', 'is_active']
    actions = [clear_rating, set_active]

admin.site.register(Post, PostAdmin)
#admin.site.register(Tag)
admin.site.register(Imajes)

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    actions = [set_active]

admin.site.register(Tag, TagAdmin)
