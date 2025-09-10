from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Bird, BirdBid, BidApproval,SellerRegistrationRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.views import is_admin 

@login_required
@user_passes_test(is_admin)
def approve_seller_request(request, request_id):
    # Fetch the seller request
    seller_request = get_object_or_404(SellerRegistrationRequest, id=request_id)

    # Approve the request
    if request.method == 'POST':
        seller_request.is_approved = True
        seller_request.approved_at = timezone.now()
        seller_request.approved_by = request.user  # Mark who approved the request
        seller_request.save()

        # Change the user role to seller
        user = seller_request.user
        user.is_seller = True
        user.is_buyer = False
        user.save()

        # Optionally, you can notify the user that their request is approved
        messages.success(request, f"{user.username} is now a seller!")

        # Redirect to the seller's dashboard after approval
        return redirect('seller:seller_dashboard')  # Updated to reflect your path

    return render(request, 'adminpanel/approve_seller_request.html', {'request_obj': seller_request})
from accounts.views import is_admin 

@login_required
@user_passes_test(is_admin)
def approve_seller_request(request, request_id):
    # Fetch the seller request
    seller_request = get_object_or_404(SellerRegistrationRequest, id=request_id)

    # Approve the request
    if request.method == 'POST':
        seller_request.is_approved = True
        seller_request.approved_at = timezone.now()
        seller_request.approved_by = request.user  # Mark who approved the request
        seller_request.save()

        # Change the user role to seller
        user = seller_request.user
        user.is_seller = True
        user.is_buyer = False
        user.save()

        # Optionally, you can notify the user that their request is approved
        messages.success(request, f"{user.username} is now a seller!")

        # Redirect to the seller's dashboard after approval
        return redirect('seller:seller_dashboard')  # Updated to reflect your path

    return render(request, 'adminpanel/approve_seller_request.html', {'request_obj': seller_request})



@login_required
def create_bird(request):
    if request.method == 'POST':
        # handle form submission
        pass
    return render(request, 'seller/create_bird.html')

@login_required
def view_bids(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    bids = BirdBid.objects.filter(bird=bird)
    return render(request, 'seller/view_bids.html', {'bids': bids})

@login_required
def approve_bid(request, bird_id, bid_id):
    bird = Bird.objects.get(id=bird_id)
    bid = BirdBid.objects.get(id=bid_id)
    BidApproval.objects.create(bird=bird, approved_buyer=bid.buyer, bid=bid)
    return redirect('seller:dashboard')

@login_required
def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')