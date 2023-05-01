# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCustomer, StripeSubscription
from stripe_integrations.webhooks.base import BaseWebhook


class CustomerSubscriptionBaseWebhook(BaseWebhook):
    def process_webhook(self):
        if self.event.validated_message:
            StripeSubscription.sync_from_stripe_data(
                self.event.customer,
                self.event.validated_message["data"]["object"],
            )

        if self.event.customer:
            StripeCustomer.sync(self.event.customer)


class CustomerSubscriptionCreatedWebhook(CustomerSubscriptionBaseWebhook):
    name = "customer.subscription.created"
    description = (
        "Occurs whenever a customer with no subscription is signed up for a plan."
    )


class CustomerSubscriptionDeletedWebhook(CustomerSubscriptionBaseWebhook):
    name = "customer.subscription.deleted"
    description = "Occurs whenever a customer ends their subscription."


class CustomerSubscriptionTrialWillEndWebhook(CustomerSubscriptionBaseWebhook):
    name = "customer.subscription.trial_will_end"
    description = "Occurs three days before the trial period of a subscription is scheduled to end."


class CustomerSubscriptionUpdatedWebhook(CustomerSubscriptionBaseWebhook):
    name = "customer.subscription.updated"
    description = "Occurs whenever a subscription changes. Examples would include switching from one plan to another, or switching status from trial to active."
