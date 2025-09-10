from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_google_user = models.BooleanField(default=False)
    google_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Permissions for this user.',
        verbose_name='user permissions',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username
