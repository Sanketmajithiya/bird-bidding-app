from django.db import models
from accounts.models import CustomUser
from seller.models import Bird,BirdBid


class BuyerAdmin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Buyer: {self.user.username}"

class BidChangeRequest(models.Model):
    bird_bid = models.ForeignKey(BirdBid, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bid_change_requests')  # seller user here
    new_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ChangeRequest({self.bird_bid.bird.name}) from {self.requested_by.username}"