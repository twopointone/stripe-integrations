# Standard Library
import logging

# Third Party Stuff
import stripe
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from stripe.error import InvalidRequestError

# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCustomer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sync (ONLY UPDATE, it doesn't create customers if not exist in local DB) customers from stripe

    command: python manage.py sync_stripe_customers
    """

    help = "Sync customers data"

    def handle(self, *args, **options):
        if not stripe.api_key:
            logger.info("Stripe API key not set")
            return

        User = apps.get_model(settings.AUTH_USER_MODEL)
        users = User.objects.all()
        total = users.count()
        count = 0

        for user in users:
            customer = StripeCustomer.get(user)

            # show percentage of local customer's synced with stripe
            if customer:
                count += 1
                percent = int(round(100 * (float(count) / float(total))))
                self.stdout.write(
                    "[{0}/{1} {2}%] Syncing {3} {4}\n".format(
                        count,
                        total,
                        percent,
                        user.first_name,
                        user.last_name,
                    )
                )

                # sync local customer with stripe
                try:
                    customer = StripeCustomer.sync(customer)
                except InvalidRequestError as exc:
                    if exc.http_status == 404:
                        # This user doesn't exist (might be in test mode)
                        logger.info(
                            "Stripe customer doesn't exist, user_id=%s, customer_id=%s",
                            user.id,
                            customer.stripe_id,
                        )
                        continue
                    raise exc
