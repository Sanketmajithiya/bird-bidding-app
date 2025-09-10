from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
def redirect_based_on_role(request):
    user = request.user
    if user.is_admin:
        return redirect('admin_dashboard')
    elif user.is_seller:
        return redirect('seller_dashboard')
    elif user.is_buyer:
        return redirect('buyer_dashboard')
    else:
        return redirect('set_role')  


def profile_view(request):
    return render(request, 'accounts/profile.html')


def custom_logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"{username}, you have been logged out successfully.")
        print(f"{username} has been logged out.")  # Backend confirmation ke liye
    else:
        print("Logout attempted but user was not logged in.")
        messages.info(request, "You were not logged in.")
    return redirect('/')
