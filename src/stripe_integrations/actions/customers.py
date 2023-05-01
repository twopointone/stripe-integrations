# Third Party Stuff
import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone

# Stripe Integrations Stuff
from stripe_integrations import utils
from stripe_integrations.settings import stripe_settings


class StripeCustomer:
    @classmethod
    def create(cls, user, billing_email, metadata=None, **kwargs):
        """
        Creates a Stripe customer.
        If a customer already exists, the existing customer will be returned.
        Args:
            user: a user object
        Returns:
            a customer object that was created
        """
        if not metadata:
            metadata = {}

        customer = cls.get(user)
        if customer:
            try:
                stripe.Customer.retrieve(customer.stripe_id)
                return customer
            except stripe.error.InvalidRequestError:
                pass

        # At this point we maybe have a local Customer but no stripe customer
        # let's create one and make the binding
        stripe_customer = stripe.Customer.create(
            email=billing_email, metadata=metadata, **kwargs
        )

        data = {
            stripe_settings.USER_FIELD_NAME: user,
            "is_active": True,
            "livemode": stripe_customer["livemode"],
            "defaults": {"stripe_id": stripe_customer["id"], "email": billing_email},
        }

        customer, created = stripe_settings.CUSTOMER_MODEL.objects.get_or_create(**data)

        if not created:
            customer.stripe_id = stripe_customer["id"]  # sync will call customer.save()

        customer = cls.sync_from_stripe_data(customer, stripe_customer)

        return customer

    @classmethod
    def get(cls, user):
        """
        Get a customer object for a given user
        Args:
                user: a user object
        Returns:
            a customer object(local customer)
        """
        if not hasattr(user, stripe_settings.CUSTOMER_FIELD_NAME):
            data = {stripe_settings.USER_FIELD_NAME: user, "is_active": True}
            customer = stripe_settings.CUSTOMER_MODEL.objects.filter(**data).first()
            setattr(user, stripe_settings.CUSTOMER_FIELD_NAME, customer)

        return getattr(user, stripe_settings.CUSTOMER_FIELD_NAME)

    @classmethod
    def sync_from_stripe_data(cls, customer, stripe_customer):
        """
        Synchronizes a local Customer object with details from the Stripe API
        Args:
            customer: a Customer object
            stripe_customer: optionally,
            data from the Stripe API representing the customer
        Returns:
            a customer object(local customer)
        """
        customer.balance = utils.convert_amount_for_db(
            stripe_customer["balance"], stripe_customer["currency"]
        )
        customer.currency = stripe_customer["currency"] or ""
        customer.delinquent = stripe_customer["delinquent"]
        customer.default_source = stripe_customer["default_source"] or ""
        customer.description = stripe_customer["description"] or ""
        customer.address = stripe_customer["address"] or ""
        customer.name = stripe_customer["name"] or ""
        customer.shipping = stripe_customer["shipping"]
        customer.tax_exempt = stripe_customer["tax_exempt"]
        customer.preferred_locales = stripe_customer["preferred_locales"]
        customer.invoice_prefix = stripe_customer["invoice_prefix"] or ""
        customer.invoice_settings = stripe_customer["invoice_settings"]
        customer.metadata = stripe_customer["metadata"]
        customer.save()

        return customer

    @classmethod
    def sync(cls, customer, stripe_customer=None):
        """
        Synchronizes a local Customer object with details from the Stripe API
        Args:
            customer: a Customer object
            stripe_customer: optionally,
            data from the Stripe API representing the customer
        Returns:
            a customer object(local customer)
        """
        if not customer.is_active:
            return

        if not stripe_customer:
            stripe_customer = stripe.Customer.retrieve(customer.stripe_id)

        if stripe_customer.get("deleted", False):
            cls.soft_delete(customer)
            return

        # Sync customer details
        customer = cls.sync_from_stripe_data(customer, stripe_customer)

        # Stripe Integrations Stuff
        from stripe_integrations.actions.sources import StripeCard
        from stripe_integrations.actions.subscriptions import StripeSubscription

        # Sync customer card details
        if customer.default_source:
            stripe_source = stripe.Customer.retrieve_source(
                customer.stripe_id, customer.default_source
            )
            StripeCard.sync_from_stripe_data(customer, source=stripe_source)

        # Sync subscription details
        subscriptions = stripe.Subscription.auto_paging_iter(
            customer=customer.stripe_id
        )
        for subscription in subscriptions:
            StripeSubscription.sync_from_stripe_data(
                customer=customer,
                stripe_subscription=subscription,
            )

        return customer

    @classmethod
    def link_customer(cls, event):
        """
        Links a customer referenced in a webhook event message to the event object
        Args:
            event: the stripe_integrations.stripe.models.Event object to link
        """

        if event.kind == "customer.created":
            return

        customer_crud_events = [
            "customer.updated",
            "customer.deleted",
        ]
        event_data_object = event.message["data"]["object"]
        if event.kind in customer_crud_events:
            stripe_customer_id = event_data_object["id"]
        else:
            stripe_customer_id = event_data_object.get("customer", None)

        if stripe_customer_id is not None:
            try:
                customer = stripe_settings.CUSTOMER_MODEL.objects.get(
                    stripe_id=stripe_customer_id
                )
            except ObjectDoesNotExist:
                raise Http404(
                    f"Stripe customer does not exist for event={event.stripe_id}"
                )

            event.customer = customer
            event.save()

        return event

    @classmethod
    def soft_delete(cls, customer):
        """
        Soft deletes the local customer object (Customer)
        Args:
            customer: Customer object
        """
        customer.is_active = False
        customer.date_purged = timezone.now()
        customer.save()
