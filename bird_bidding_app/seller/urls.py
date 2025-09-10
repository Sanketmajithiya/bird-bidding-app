from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('create/', views.create_bird, name='create_bird'),
    path('bids/<int:bird_id>/', views.view_bids, name='view_bids'),
    path('approve/<int:bird_id>/<int:bid_id>/', views.approve_bid, name='approve_bid'),
    path('seller/add-bird/', views.create_bird, name='add_bird'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
]
