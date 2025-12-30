from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created.

    Note: This runs within the same database transaction as the User save,
    ensuring atomic creation of User and Profile together.
    """
    if created:
        from accounts.models import Profile

        Profile.objects.create(user=instance)
