# Webhook

Listen for events on your Stripe account so your integration can automatically trigger reactions.

Stripe uses webhooks to notify your application when an event happens in your account. Webhooks are particularly useful for asynchronous events like when a customer’s bank confirms a payment, a customer disputes a charge, a recurring payment succeeds, or when collecting subscription payments.

A webhook enables Stripe to push real-time notifications to your app. Stripe uses HTTPS to send these notifications to your app as a JSON payload. You can then use these notifications to execute actions in your backend systems.

## Webhook events

Following are the supported webhook events:

* **Customer:** `stripe_integrations.webhooks.customers` contains all the customer related webhook event
    * Create customer: `CustomerCreatedWebhook` will process the `customer.created` webhook event.
    * Update customer: `CustomerUpdatedWebhook` will process the `customer.updated` webhook event.
    * Delete customer: `CustomerDeletedWebhook` will process the `customer.deleted` webhook event.
* **Card:** `stripe_integrations.webhooks.sources` contains all the card related webhook event
    * Create card: `CustomerSourceCreatedWebhook` will process the `customer.source.created` webhook event.
    * Update card: `CustomerSourceUpdatedWebhook` will process the `customer.source.updated` webhook event.
    * Delete card: `CustomerSourceDeletedWebhook` will process the `customer.source.deleted` webhook event.
* **Subscription:** `stripe_integrations.webhooks.subscriptions` contains all the subscriptions related webhook event
    * Create subscription: `CustomerSubscriptionCreatedWebhook` will process the `customer.subscription.created"` webhook event.
    * Update subscription: `CustomerSubscriptionUpdatedWebhook` will process the `customer.subscription.updated"` webhook event.
    * Subscription trial will end: `CustomerSubscriptionTrialWillEndWebhook` will process the `customer.subscription.trial_will_end"` webhook event.
    * Delete subscription: `CustomerSubscriptionDeletedWebhook` will process the `customer.subscription.deleted"` webhook event.
* **Product:** `stripe_integrations.webhooks.products` contains all the product related webhook event
    * Create product: `ProductCreatedWebhook` will process the `product.created` webhook event.
    * Update product: `ProductUpdatedWebhook` will process the `product.updated` webhook event.
    * Delete product: `ProductDeletedWebhook` will process the `product.deleted` webhook event.
* **Price:** `stripe_integrations.webhooks.prices` contains all the price related webhook event
    * Create price: `PriceCreatedWebhook` will process the `price.created` webhook event.
    * Update price: `PriceUpdatedWebhook` will process the `price.updated` webhook event.
    * Delete price: `PriceDeletedWebhook` will process the `price.deleted` webhook event.
* **Coupon:** `stripe_integrations.webhooks.coupons` contains all the coupon related webhook event
    * Create coupon: `CouponCreatedWebhook` will process the `coupon.created` webhook event.
    * Update coupon: `CouponUpdatedWebhook` will process the `coupon.updated` webhook event.
    * Delete coupon: `CouponDeletedWebhook` will process the `coupon.deleted` webhook event.

## Configure Webhook

Create a view-set that will use [StripeWebhook](/library/actions/webhooks) action to process the webhook event.

!!! Example "Create webhook viewset"
    ```python
    from django.http import Http404
    from rest_framework import viewsets
    from rest_framework.permissions import AllowAny

    from stripe_integrations.actions import StripeWebhook
    from project.base import response
    from payment.models import Event


    class StripeWebhookViewSet(viewsets.GenericViewSet):
        EVENT_MODEL = Event

        # Check the webhook signatures
        # Ref: https://stripe.com/docs/webhooks/signatures

        def create(self, request, *args, **kwargs):
            try:
                event_data = request.data
                StripeWebhook.process_webhook(event_data)
            except Http404 as e:
                raise e
            return response.Ok({"success": True})
    ```

!!! Example "Register webhook view-set to an endpoint"
    ```python
    from rest_framework.routers import DefaultRouter

    from payments.apis import StripeWebhookViewSet


    default_router = DefaultRouter(trailing_slash=False)

    default_router.register(
        "stripe/webhook", StripeWebhookViewSet, basename="stripe-webhook"
    )
    ```

## Custom Webhook Event

To create a custom webhook event for a specific Stripe webhook event, you can inherit `BaseWebhook` from `stripe_integrations.webhooks.base` and implement your own webhook event processing logic.

As an example, let's say you want to create a webhook event for the product.created event. You can create a new file`app/webhook/products.py` and define the webhook event class in it.

!!! Example
    ```
    # Stripe Integrations Stuff
    from stripe_integrations.actions import StripeProduct
    from stripe_integrations.webhooks.base import BaseWebhook


    class ProductCreateWebhook(BaseWebhook):
        name = "product.created"
        description = "Occurs whenever a new product is created."

        def process_webhook(self):
            StripeProduct.sync(self.event.message["data"]["object"])
    ```

Once you have implemented the webhook event, you should import the webhook file in the `__init__.py` file of the app. This is required for the webhook event class to be registered.

!!! Example
    ```
    import importlib

    importlib.import_module("app.webhooks.products")
    ```

!!! Note
    If the class is not registered, then the webhook event won't be processed.
