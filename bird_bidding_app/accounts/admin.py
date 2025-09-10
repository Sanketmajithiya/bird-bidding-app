from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_buyer', 'is_seller', 'is_admin', 'is_google_user', 'created_at')
    list_filter = ('is_buyer', 'is_seller', 'is_admin', 'is_google_user')
    search_fields = ('username', 'email', 'google_email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'is_buyer', 'is_seller', 'is_admin', 'is_google_user', 'google_email')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
