from logging import getLogger

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from sqlalchemy import select
from sqlalchemy.orm import Session

from analytics.orm import TraderOrm
from db import engine

from .models import User, UserProfile

logging = getLogger("authusers.signals")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance: User, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        with Session(engine) as session:
            trader = session.execute(
                select(TraderOrm)
                .where(TraderOrm.trader_id == instance.username)
                .order_by(TraderOrm.branch_name)
            ).scalar_one_or_none()
            if trader:
                logging.info(f"profile info found for {instance!r}")
                profile.branch_id = trader.branch_code
                profile.branch_name = trader.branch_name
                instance.first_name = trader.trader_name
                logging.info(f"profile info setup finished for {instance}")
            else:
                logging.info(f"'!!!' profile info not found for {instance!r} '!!!'")
        profile.save()
        logging.info(f"profile has been saved for {instance!r}")
