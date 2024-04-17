from django.contrib import admin
from  .models import Category, Post, Tag, Imajes
# Register your models here.

admin.site.register(Category)


def clear_rating(modeladmin, request, queryset):
    queryset.update(rating=1)


clear_rating.short_description = "Выставить рейтинг = 1"

class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'category', 'display_tags', 'has_image', 'rating']
    actions = [clear_rating]

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Imajes)


