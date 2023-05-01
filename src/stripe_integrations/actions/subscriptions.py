# Third Party Stuff
import stripe
from django.db.models import Q
from django.utils import timezone

# Stripe Integrations Stuff
from stripe_integrations import utils
from stripe_integrations.actions.customers import StripeCustomer
from stripe_integrations.settings import stripe_settings


class StripeSubscription:
    @classmethod
    def create(cls, customer, prices, coupon=None, trial_from_plan=True):
        """
        Creates a subscription for the given customer
        Args:
            customer: the customer to create the subscription for
            price: the pricing of product to subscribe to
        Returns:
            the stripe_integrations.stripe.models.Subscription
            object (created or updated)
        """

        subscription_params = {}
        subscription_params["customer"] = customer.stripe_id
        subscription_params["items"] = list(map(lambda price: {"price": price}, prices))

        # Indicates if a price’s trial_period_days should be applied to the subscription
        # Ref: https://stripe.com/docs/api/subscriptions/create#create_subscription-trial_from_plan
        options = {
            "trial_from_plan": trial_from_plan,
        }

        # Apply coupon to subscription
        if coupon:
            subscription_params["coupon"] = coupon.stripe_id

        stripe_subscription = stripe.Subscription.create(
            **subscription_params, **options
        )
        subscription = cls.sync_from_stripe_data(customer, stripe_subscription)

        return subscription

    @classmethod
    def update(cls, subscription, price, pro_rate=True):
        """
        Updates a subscription
        Args:
            subscription: the subscription to be updated
            price: the new pricing obj of product to subscribe to
            pro_rate: Whether to prorate Subscription charges
        Ref Docs: https://stripe.com/docs/api/subscriptions/update
        """

        if pro_rate:
            # prorate charges in next billing cycle
            proration_behavior = "create_prorations"
        else:
            # Do not prorate, update subscription from next billing cycle
            proration_behavior = "none"

        items = [{"id": subscription.items["data"][0]["id"], "price": price.stripe_id}]
        stripe_subscription = stripe.Subscription.modify(
            subscription.stripe_id, proration_behavior=proration_behavior, items=items
        )
        return cls.sync_from_stripe_data(
            getattr(subscription, stripe_settings.CUSTOMER_FIELD_NAME),
            stripe_subscription,
        )

    @classmethod
    def cancel(cls, subscription, cancel_immediately=False):
        """
        Cancels the subscription at the end of the current billing period
        Ref Docs: https://stripe.com/docs/api/subscriptions/cancel
        Args:
            subscription: the subscription obj to cancel
        """

        if cancel_immediately:
            stripe_subscription = stripe.Subscription.delete(subscription.stripe_id)
        else:
            stripe_subscription = stripe.Subscription.modify(
                subscription.stripe_id, cancel_at_period_end=True
            )

        return cls.sync_from_stripe_data(
            getattr(subscription, stripe_settings.CUSTOMER_FIELD_NAME),
            stripe_subscription,
        )

    @classmethod
    def sync_from_stripe_data(cls, customer, stripe_subscription):
        """
        Synchronizes data from the Stripe API for a subscription
        Args:
            customer: the customer who's subscription we are syncronizing
            stripe_subscription: data from the Stripe API representing
            a subscription
        Returns:
            the stripe_integrations.models.Subscription object (created or updated)
        """
        defaults = dict(
            items=stripe_subscription["items"],
            application_fee_percent=stripe_subscription["application_fee_percent"],
            automatic_tax=dict(stripe_subscription["automatic_tax"]),
            billing_cycle_anchor=utils.convert_tstamp(
                stripe_subscription["billing_cycle_anchor"]
            ),
            billing_thresholds=stripe_subscription["billing_thresholds"],
            cancel_at=utils.convert_tstamp(stripe_subscription["cancel_at"]),
            cancel_at_period_end=stripe_subscription["cancel_at_period_end"],
            canceled_at=utils.convert_tstamp(stripe_subscription["canceled_at"]),
            cancellation_details=dict(stripe_subscription["cancellation_details"]),
            current_period_start=utils.convert_tstamp(
                stripe_subscription["current_period_start"]
            ),
            current_period_end=utils.convert_tstamp(
                stripe_subscription["current_period_end"]
            ),
            collection_method=stripe_subscription["collection_method"],
            days_until_due=stripe_subscription["days_until_due"],
            default_payment_method=stripe_subscription["default_payment_method"] or "",
            default_source=stripe_subscription["default_source"] or "",
            default_tax_rates=stripe_subscription["default_tax_rates"],
            discount=stripe_subscription["discount"],
            ended_at=utils.convert_tstamp(stripe_subscription["ended_at"]),
            next_pending_invoice_item_invoice=utils.convert_tstamp(
                stripe_subscription["next_pending_invoice_item_invoice"]
            ),
            pause_collection=stripe_subscription["pause_collection"],
            pending_invoice_item_interval=stripe_subscription[
                "pending_invoice_item_interval"
            ],
            pending_setup_intent=stripe_subscription["pending_setup_intent"] or "",
            pending_update=stripe_subscription["pending_update"],
            quantity=stripe_subscription["quantity"],
            start_date=utils.convert_tstamp(stripe_subscription["start_date"]),
            status=stripe_subscription["status"],
            trial_start=utils.convert_tstamp(stripe_subscription["trial_start"]),
            trial_end=utils.convert_tstamp(stripe_subscription["trial_end"]),
            latest_invoice=stripe_subscription["latest_invoice"] or "",
        )
        defaults.update({stripe_settings.CUSTOMER_FIELD_NAME: customer})

        subscription, _ = stripe_settings.SUBSCRIPTION_MODEL.objects.update_or_create(
            stripe_id=stripe_subscription["id"], defaults=defaults
        )
        return subscription

    @classmethod
    def has_active_subscription(cls, customer):
        """
        Checks if the given customer has an active subscription
        Args:
            customer: the customer to check
        Returns:
            True, if there is an active subscription, otherwise False
        """
        data = {stripe_settings.CUSTOMER_FIELD_NAME: customer}

        if customer:
            return (
                stripe_settings.SUBSCRIPTION_MODEL.objects.filter(**data)
                .filter(Q(ended_at__isnull=True) | Q(ended_at__gt=timezone.now()))
                .exists()
            )
        return None

    @classmethod
    def get_current_subscription(cls, user, customer=None):
        """
        Get current subscription obj for a given user
        Args:
            user: a user object
            customer: a stripe customer object
        Returns:
            a user subscription object
        """
        if not customer:
            customer = StripeCustomer.get(user)

        data = {stripe_settings.CUSTOMER_FIELD_NAME: customer}
        current_subscription = stripe_settings.SUBSCRIPTION_MODEL.objects.filter(
            status__in=stripe_settings.SUBSCRIPTION_MODEL.STATUS_CURRENT, **data
        ).first()
        return current_subscription

    @classmethod
    def get_subscription(cls, user, customer=None):
        """
        Get subscription obj for a given user
        Args:
            user: a user object
            customer: a stripe customer object
        Returns:
            a user subscription object
        """
        if not customer:
            customer = StripeCustomer.get(user)

        # check for active subscription
        data = {stripe_settings.CUSTOMER_FIELD_NAME: customer}
        subscription = stripe_settings.SUBSCRIPTION_MODEL.objects.filter(
            status__in=stripe_settings.SUBSCRIPTION_MODEL.STATUS_CURRENT, **data
        ).first()

        # if there is no active subscription then send the latest subscription object
        if not subscription:
            subscription = (
                stripe_settings.SUBSCRIPTION_MODEL.objects.filter(**data)
                .order_by("-created_at")
                .first()
            )

        return subscription

    @classmethod
    def get_stripe_subscription(cls, subscription):
        """
        Get stripe subscription obj for a given subscription
        Args:
            subscription: a subscription object
        Returns:
            a stripe subscription object
        """
        return stripe.Subscription.retrieve(subscription.stripe_id)

    @classmethod
    def get_upcoming_invoice(cls, subscription):
        """
        Get upcoming stripe invoice obj for a given subscription
        Args:
            subscription: a subscription object
        Returns:
            a stripe invoice object
        """
        return stripe.Invoice.upcoming(subscription=subscription.stripe_id)

    @classmethod
    def get_latest_invoice(cls, subscription):
        """
        Get latest stripe invoice obj for a given subscription
        Args:
            subscription: a subscription object
        Returns:
            a stripe invoice object
        """
        return stripe.Invoice.retrieve(subscription.latest_invoice)
