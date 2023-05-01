# Stripe Integrations Stuff
from stripe_integrations.actions import StripeProduct
from stripe_integrations.webhooks.base import BaseWebhook


class ProductBaseWebhook(BaseWebhook):
    def process_webhook(self):
        StripeProduct.sync(self.event.message["data"]["object"])


class ProductCreatedWebhook(ProductBaseWebhook):
    name = "product.created"
    description = "Occurs whenever a new product is created."


class ProductUpdatedWebhook(ProductBaseWebhook):
    name = "product.updated"
    description = "Occurs whenever any property of a product changes."


class ProductDeletedWebhook(BaseWebhook):
    name = "product.deleted"
    description = "Occurs whenever a product is deleted."

    def process_webhook(self):
        StripeProduct.soft_delete(self.event.validated_message["data"]["object"]["id"])
