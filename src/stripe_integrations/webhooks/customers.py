# Third Party Stuff
from django.apps import apps
from django.conf import settings

# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCustomer
from stripe_integrations.settings import stripe_settings
from stripe_integrations.webhooks.base import BaseWebhook


class CustomerUpdatedWebhook(BaseWebhook):
    name = "customer.updated"
    description = "Occurs whenever any property of a customer changes."

    def process_webhook(self):
        if self.event.customer:
            stripe_customer = self.event.message["data"]["object"]
            StripeCustomer.sync(self.event.customer, stripe_customer)


class CustomerCreatedWebhook(BaseWebhook):
    name = "customer.created"
    description = "Occurs whenever a new customer is created."

    def process_webhook(self):
        stripe_customer = self.event.message["data"]["object"]
        email = stripe_customer["email"]
        stripe_id = self.event.message["data"]["object"]["id"]
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User.objects.filter(email=email).first()

        if user and not user.stripe_customers.exists():
            # create customer
            data = {
                "user": user,
                "email": user.email,
                "is_active": True,
                "defaults": {"stripe_id": stripe_id},
            }
            customer, _ = stripe_settings.CUSTOMER_MODEL.objects.get_or_create(**data)

            # link customer to event
            self.event.customer = customer
            self.event.save()

            # sync customer
            StripeCustomer.sync(customer, stripe_customer)


class CustomerDeletedWebhook(BaseWebhook):
    name = "customer.deleted"
    description = "Occurs whenever a customer is deleted."

    def process_webhook(self):
        if self.event.customer:
            StripeCustomer.soft_delete(self.event.customer)
