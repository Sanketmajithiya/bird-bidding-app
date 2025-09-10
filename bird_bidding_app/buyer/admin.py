from django.contrib import admin
from .models import BidChangeRequest


@admin.register(BidChangeRequest)
class BidChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'bird_bid',
        'requested_by',
        'new_amount',
        'is_approved',
        'approved_by',
        'requested_at',
        'approved_at',
    )
    list_filter = ('is_approved',)
    search_fields = ('bird_bid__bird__name', 'requested_by__username', 'approved_by__username')
    readonly_fields = ('requested_at', 'approved_at')


