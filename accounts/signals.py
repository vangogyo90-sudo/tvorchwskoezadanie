from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def ensure_user_profile(sender, instance, created, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=instance)
    if instance.is_superuser and profile.role != Profile.ROLE_ADMIN:
        profile.role = Profile.ROLE_ADMIN
        profile.save(update_fields=("role", "updated_at"))
