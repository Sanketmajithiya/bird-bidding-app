from django.contrib import messages
from django.shortcuts import render, redirect
from seller.models import Bird, BirdBid, SellerRegistrationRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# buyer beacome seller
@login_required
def become_seller(request):
    user = request.user

    # If the user is already a seller, inform them and redirect
    if user.is_seller:
        messages.info(request, "You are already a seller.")
        return redirect('seller:seller_dashboard')

    # Check if there is already a pending seller registration request
    existing_request = SellerRegistrationRequest.objects.filter(user=user, is_approved=False).first()
    if existing_request:
        messages.info(request, "Your request to become a seller is already pending. Please wait for approval.")
        return redirect('buyer:bird_list')

    # If POST request, create a new seller registration request
    if request.method == 'POST':
        SellerRegistrationRequest.objects.create(user=user)
        messages.success(request, "Your request to become a seller has been sent to the admin.")
        return redirect('buyer:bird_list')

    # If GET request, render the become seller request page with a form
    return render(request, 'buyer/become_seller.html')

@login_required
def bird_list(request):
    # Get search query from GET parameters (default is an empty string)
    search_query = request.GET.get('q', '')

    # Start with all birds
    birds = Bird.objects.all()

    # Apply search filter if a search query is provided
    if search_query:
        birds = birds.filter(
            name__icontains=search_query  # Search by bird name
        ) | birds.filter(
            age__icontains=search_query  # Search by age
        ) | birds.filter(
            color__icontains=search_query  # Search by color
        ) | birds.filter(
            price__icontains=search_query  # Search by price
        )

    # Annotate the birds with like count and order by the likes
    birds = birds.annotate(likes_count=Count('likes')).order_by('-likes_count')

    # Return the birds with the search query in context
    return render(request, 'buyer/bird_list.html', {
        'birds': birds,
        'search_query': search_query,  # Send the search query back to the template
    })

@login_required
def like_bird(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    user = request.user._wrapped  # Get the actual user instance
    if user not in bird.likes.all():
        bird.likes.add(user)
    return redirect('buyer:bird_list')


@login_required
def bid_bird(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        BirdBid.objects.create(bird=bird, buyer=request.user, amount=amount)
        return redirect('buyer:bird_list')
    highest_bid = BirdBid.objects.filter(bird=bird).order_by('-amount').first()
    return render(request, 'buyer/bid_bird.html', {'bird': bird, 'highest_bid': highest_bid})
