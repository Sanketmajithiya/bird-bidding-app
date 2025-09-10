# adminpanel/urls.py
from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Only keep this one
    path('approve-request/<int:request_id>/', views.approve_change_request, name='approve_change_request'),
    path('seller-requests/', views.admin_dashboard, name='seller_requests_list'),  # Show pending seller requests in the dashboard
    path('approve-seller-request/<int:request_id>/', views.approve_seller_request, name='approve_seller_request'),
    path('reject-seller-request/<int:request_id>/', views.reject_seller_request, name='reject_seller_request'),
    # path('approve/<int:bird_id>/<int:bid_id>/', views.approve_bid, name='approve_bid'),
    path('approve/<int:bird_id>/<int:bid_id>/', views.approve_bid, name='approve_bid'),


]

