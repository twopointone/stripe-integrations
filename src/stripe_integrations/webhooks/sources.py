# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCard
from stripe_integrations.webhooks.base import BaseWebhook


class CustomerSourceBaseWebhook(BaseWebhook):
    def process_webhook(self):
        StripeCard.sync_from_stripe_data(
            self.event.customer, self.event.validated_message["data"]["object"]
        )


class CustomerSourceCreatedWebhook(CustomerSourceBaseWebhook):
    name = "customer.source.created"
    description = "Occurs whenever a new source is created for the customer."


class CustomerSourceDeletedWebhook(BaseWebhook):
    name = "customer.source.deleted"
    description = "Occurs whenever a source is removed from a customer."

    def process_webhook(self):
        StripeCard.delete(self.event.validated_message["data"]["object"]["id"])


class CustomerSourceUpdatedWebhook(CustomerSourceBaseWebhook):
    name = "customer.source.updated"
    description = "Occurs whenever a source's details are changed."
