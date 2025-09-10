from django.contrib import admin
from .models import BidApprovalChangeRequest



@admin.register(BidApprovalChangeRequest)
class BidApprovalChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'bird', 'requested_by', 'current_approved_bid', 'requested_new_bid',
        'is_approved', 'approved_by', 'requested_at', 'approved_at'
    )
    list_filter = ('is_approved',)
    search_fields = ('bird__name', 'requested_by__username', 'approved_by__username')
    readonly_fields = ('requested_at', 'approved_at')