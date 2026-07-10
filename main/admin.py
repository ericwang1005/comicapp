from django.contrib import admin

from main.models import Comic


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'new_update', 'fetched_at')
    search_fields = ('title',)
