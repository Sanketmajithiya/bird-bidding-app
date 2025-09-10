from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from allauth.socialaccount.models import SocialLogin
from accounts.models import CustomUser
from django.db import IntegrityError

@receiver(pre_social_login)
def social_login_handler(sender, request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':  # Only handle Google login
        email = sociallogin.account.extra_data.get('email')  # Get the email from the social account data

        try:
            # Check if the user already exists in CustomUser model
            user = CustomUser.objects.get(email=email)
            sociallogin.user = user  # Link the existing user to the social login
        except CustomUser.DoesNotExist:
            # If no user exists, you could either create a new user or handle it differently
            # For example, create a new user
            user = CustomUser.objects.create(
                username=sociallogin.account.extra_data.get('name'),
                email=email,
                is_google_user=True
            )
            sociallogin.user = user  # Link the newly created user to the social login
