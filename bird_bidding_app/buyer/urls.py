from django.urls import path
from . import views

app_name = 'buyer'  # Important for using 'buyer:bird_list' in your views

urlpatterns = [
    path('', views.bird_list, name='bird_list'),
    path('like/<int:bird_id>/', views.like_bird, name='like_bird'),
    path('bid/<int:bird_id>/', views.bid_bird, name='bid_bird'),
    path('become-seller/', views.become_seller, name='become_seller'),
    
]
