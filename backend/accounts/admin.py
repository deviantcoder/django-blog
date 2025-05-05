from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = (
        'username', 'email', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'created'
    )

    list_filter = (
        'is_active', 'is_staff', 'email_verified'
    )

    search_fields = (
        'username', 'email',
    )

    ordering = ('-created',)

    readonly_fields = ('created', 'updated')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_verified',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'email_verified'),
        }),
    )
