from django.contrib import admin
from django.utils.html import format_html
from .models import Bird, BirdBid, BidApproval, SellerRegistrationRequest


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'age', 'color', 'category', 'price', 'can_fly', 'created_at', 'image_tag')
    list_filter = ('color', 'category', 'can_fly')
    search_fields = ('name', 'seller__username', 'description')
    readonly_fields = ('created_at', 'image_tag')
    ordering = ('-created_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:contain;" />', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Preview'


@admin.register(BirdBid)
class BirdBidAdmin(admin.ModelAdmin):
    list_display = ('bird', 'buyer', 'amount', 'bid_time')
    list_filter = ('bird__category',)
    search_fields = ('bird__name', 'buyer__username')
    ordering = ('-amount', '-bid_time')


@admin.register(BidApproval)
class BidApprovalAdmin(admin.ModelAdmin):
    list_display = ('bird', 'approved_buyer', 'bid')
    search_fields = ('bird__name', 'approved_buyer__username')


@admin.register(SellerRegistrationRequest)
class SellerRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_at', 'is_approved', 'approved_at', 'approved_by')
    list_filter = ('is_approved',)
    search_fields = ('user__username',)
    ordering = ('-requested_at',)

    def approve_request(self, obj):
        if obj.is_approved:
            return "Approved"
        return "Pending"
    approve_request.short_description = 'Approval Status'