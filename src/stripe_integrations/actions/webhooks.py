# Standard Library
import logging

# Third Party Stuff
import stripe
from django.utils.encoding import smart_str
from stripe.error import InvalidRequestError

# Stripe Integrations Stuff
from stripe_integrations.actions.events import StripeEvent
from stripe_integrations.settings import stripe_settings

logger = logging.getLogger(__name__)


class StripeWebhook:
    @classmethod
    def process_webhook(cls, event_data):
        event = stripe_settings.EVENT_MODEL.objects.filter(
            stripe_id=event_data["id"]
        ).first()

        if event:
            logger.info(
                "Found duplicate stripe event record with event_id=%s", event.id
            )
            return

        if stripe.api_key:
            try:
                # create an event and process webhook
                StripeEvent.add(
                    stripe_id=event_data["id"],
                    kind=event_data["type"],
                    livemode=event_data["livemode"],
                    message=event_data,
                    api_version=event_data["api_version"],
                    request=event_data["request"],
                    pending_webhooks=event_data["pending_webhooks"],
                )
            except InvalidRequestError as e:
                event_id = event_data["id"]
                logger.info(
                    f"Error occurred while processing stripe webhook, event_id={event_id}, error={smart_str(e)}"
                )
            return

        logger.info("Stripe API key not set while creating event")

        return
