# Standard Library
import logging

# Third Party Stuff
import stripe
from django.core.management import BaseCommand

# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCoupon

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync (UPDATE_OR_CREATE in local DB) soupons from stripe

    command: python manage.py sync_stripe_coupons
    """

    help = "Sync coupons"

    def handle(self, *args, **options):
        if not stripe.api_key:
            logger.info("Stripe API key not set while syncing coupons")
            return

        StripeCoupon.sync_all()
        logger.info("Synced stripe coupons")
