from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'created')

    search_fields = ('display_name', 'user__username')

    ordering = ('-created',)

    readonly_fields = ('created', 'updated')
