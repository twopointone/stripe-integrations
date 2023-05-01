# Stripe Integrations Stuff
from stripe_integrations.actions import StripeCoupon
from stripe_integrations.webhooks.base import BaseWebhook


class CouponBaseWebhook(BaseWebhook):
    def process_webhook(self):
        StripeCoupon.sync(self.event.message["data"]["object"])


class CouponCreatedWebhook(CouponBaseWebhook):
    name = "coupon.created"
    description = "Occurs whenever a new coupon is created."


class CouponUpdatedWebhook(CouponBaseWebhook):
    name = "coupon.updated"
    description = "Occurs whenever any property of a coupon changes."


class CouponDeletedWebhook(CouponBaseWebhook):
    name = "coupon.deleted"
    description = "Occurs whenever a coupon is deleted."

    def process_webhook(self):
        StripeCoupon.soft_delete(self.event.validated_message["data"]["object"]["id"])
