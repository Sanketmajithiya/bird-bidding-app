from django.urls import path
from .views import custom_logout_view
from . import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
     path('logout/', custom_logout_view, name='account_logout'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # Add more custom account URL routes
]
