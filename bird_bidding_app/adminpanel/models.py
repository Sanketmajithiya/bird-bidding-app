from django.db import models
from accounts.models import CustomUser
from seller.models import Bird, BirdBid

# Seller wants to change previously approved bid
class BirdAdmin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin: {self.user.username}"

class BidApprovalChangeRequest(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    current_approved_bid = models.ForeignKey(BirdBid, on_delete=models.CASCADE, related_name='current_approval_request')
    requested_new_bid = models.ForeignKey(BirdBid, on_delete=models.CASCADE, related_name='requested_new_approval')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approval_change_requests')
    reason = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_change_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Change Approval Request for {self.bird.name} by {self.requested_by.username}"
    
    class BidApprovalChangeRequest(models.Model):
        def save(self, *args, **kwargs):
            # Validation: Only seller can request
            if not self.requested_by.is_seller:
                raise ValueError("Only sellers can request approval changes.")
            super().save(*args, **kwargs)

