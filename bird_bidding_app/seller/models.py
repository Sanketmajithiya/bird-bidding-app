from django.db import models
from accounts.models import CustomUser
from enumfields import EnumField
from enum import Enum


# Enums
class BirdColor(Enum):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    WHITE = 'White'
    BLACK = 'Black'
    BROWN = 'Brown'

class BirdCategory(Enum):
    PARROT = 'Parrot'
    PIGEON = 'Pigeon'
    SPARROW = 'Sparrow'
    EAGLE = 'Eagle'

class SellerAdmin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Seller: {self.user.username}"

# Bird Model (Posted by Seller)
class Bird(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='birds')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    color = EnumField(BirdColor, max_length=20)
    category = EnumField(BirdCategory, max_length=20)
    image = models.ImageField(upload_to='birds/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.FloatField(help_text="Weight in kg")
    can_fly = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_birds', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.seller.username}"

#  Bid Model (By Buyer)
class BirdBid(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bird.name} - {self.amount} by {self.buyer.username}"

    def save(self, *args, **kwargs):
        # Validation: Only Buyers can bid
        if not self.buyer.is_buyer:
            raise ValueError("Only users with buyer role can place bids.")
        super().save(*args, **kwargs)


#  Buyer Approval (One seller approves one buyer's bid)
class BidApproval(models.Model):
    bird = models.OneToOneField(Bird, on_delete=models.CASCADE)
    approved_buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bid = models.OneToOneField(BirdBid, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bird.name} Approved to {self.approved_buyer.username}"


# convert to beacome buyer to seller
class SellerRegistrationRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # user who wants to be seller
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='seller_requests_approved')

    def __str__(self):
        return f"Seller Registration Request by {self.user.username}"
