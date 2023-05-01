# Stripe Integrations Stuff
from stripe_integrations.actions import StripePrice
from stripe_integrations.webhooks.base import BaseWebhook


class PriceBaseWebhook(BaseWebhook):
    def process_webhook(self):
        StripePrice.sync(self.event.message["data"]["object"])


class PriceCreatedWebhook(PriceBaseWebhook):
    name = "price.created"
    description = "Occurs whenever a new price is created."


class PriceUpdatedWebhook(PriceBaseWebhook):
    name = "price.updated"
    description = "Occurs whenever any property of a price changes."


class PriceDeletedWebhook(PriceBaseWebhook):
    name = "price.deleted"
    description = "Occurs whenever a price is deleted."

    def process_webhook(self):
        StripePrice.soft_delete(self.event.validated_message["data"]["object"]["id"])
