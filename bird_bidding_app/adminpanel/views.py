# adminpanel/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from adminpanel.models import BidApprovalChangeRequest
from seller.models import BidApproval,Bird,SellerRegistrationRequest
from django.utils import timezone

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def approve_bid(request, bird_id, bid_id):
    # Fetch the bird and the bid
    bird = get_object_or_404(Bird, id=bird_id)
    bid = get_object_or_404(BidApproval, id=bid_id)

    # Process for approving the bid
    if request.method == 'POST':
        # Your logic to approve the bid, e.g., change the status, etc.
        bid.is_approved = True
        bid.save()
        return redirect('adminpanel:admin_dashboard')
    return render(request, 'adminpanel/approve_request.html', {'bird': bird, 'bid': bid})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    seller_requests = SellerRegistrationRequest.objects.filter(is_approved=False)
    change_requests = BidApprovalChangeRequest.objects.filter(is_approved=False)
    birds = Bird.objects.all()

    # Fetching all bids related to birds
    bids = BidApproval.objects.filter(bird__in=birds)

    return render(request, 'adminpanel/dashboard.html', {
        'birds': birds,
        'change_requests': change_requests,
        'seller_requests': seller_requests,
        'bids': bids,  # Make sure to pass bids to the template
    })

@login_required
@user_passes_test(lambda u: u.is_admin)
def approve_change_request(request, request_id):
    req = get_object_or_404(BidApprovalChangeRequest, id=request_id)

    if request.method == 'POST':
        req.is_approved = True
        req.approved_by = request.user
        req.approved_at = timezone.now()
        req.save()

        # Update actual approval
        approval = BidApproval.objects.get(bird=req.bird)
        approval.bid = req.requested_new_bid
        approval.approved_buyer = req.requested_new_bid.buyer
        approval.save()

        return redirect('admin_dashboard')

    return render(request, 'adminpanel/approve_request.html', {'request_obj': req})


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

        return redirect('adminpanel:admin_dashboard')

    return render(request, 'adminpanel/approve_seller_request.html', {'request_obj': seller_request})



@login_required
@user_passes_test(is_admin)
def reject_seller_request(request, request_id):
    # Fetch the seller request
    seller_request = get_object_or_404(SellerRegistrationRequest, id=request_id)

    # Reject the request
    if request.method == 'POST':
        seller_request.is_approved = False
        seller_request.rejected_at = timezone.now()  # Add a rejection timestamp (optional)
        seller_request.rejected_by = request.user  # Who rejected the request
        seller_request.save()

        # Optionally, you can notify the user that their request is rejected
        messages.error(request, f"{seller_request.user.username}'s registration request has been rejected.")

        return redirect('adminpanel:admin_dashboard')

    return render(request, 'adminpanel/reject_seller_request.html', {'request_obj': seller_request})
