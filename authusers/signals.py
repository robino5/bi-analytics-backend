from logging import getLogger

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Trader, User, UserProfile

logging = getLogger("authusers.signals")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance: User, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        trader = Trader.objects.filter(trader_id=instance.username).first()
        if trader:
            logging.info(f"profile info found for {instance!r}")
            profile.branch_id = trader.branch_code
            profile.branch_name = trader.branch_name
            instance.first_name = trader.trader_name
            profile.save()
            instance.save()
            logging.info(f"profile info updated for {instance}")
