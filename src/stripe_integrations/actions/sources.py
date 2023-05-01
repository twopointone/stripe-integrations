# Third Party Stuff
import stripe

# Stripe Integrations Stuff
from stripe_integrations.actions.customers import StripeCustomer
from stripe_integrations.settings import stripe_settings


class StripeCard:
    @classmethod
    def set_default_card(cls, customer, card_token):
        """
        Create a new source object, make it the new customer default source,
        and delete the old customer default if one exists
        Args:
            customer: the customer to update the source for
            card_token: the token created from Stripe.js
        Update Customer default sourceDocs: https://stripe.com/docs/api/customers/update?lang=python
        Retrieve Card Docs: https://stripe.com/docs/api/cards/retrieve?lang=python
        """
        stripe_customer = stripe.Customer.modify(customer.stripe_id, source=card_token)

        # sync customer from stripe to update default source
        StripeCustomer.sync_from_stripe_data(customer, stripe_customer)
        source = stripe.Customer.retrieve_source(
            customer.stripe_id, stripe_customer["default_source"]
        )

        return cls.sync_from_stripe_data(customer, source)

    @classmethod
    def delete_card(cls, customer, source_stripe_id):
        """
        Deletes a card from a customer
        Args:
            customer: the customer to delete the card from
            source_stripe_id: the Stripe ID of the payment source to delete
        Ref Docs: https://stripe.com/docs/api/cards/delete
        """
        stripe.Customer.delete_source(customer.stripe_id, source_stripe_id)

        # sync customer from stripe to update default source
        StripeCustomer.sync(customer)

        return cls.delete(source_stripe_id)

    @classmethod
    def sync_from_stripe_data(cls, customer, source):
        """
        Synchronizes the data for a payment source locally for a given customer

        Args:
            customer: the customer to create or update a Bitcoin receiver for
            source: data representing the payment source from the Stripe API
        """
        if source["object"] == "card":
            return cls.sync(customer, source)

    @classmethod
    def sync(cls, customer, source=None):
        """
        Synchronizes the data for a card locally for a given customer

        Args:
            customer: the customer to create or update a card for
            source: data representing the card from the Stripe API
        """
        defaults = dict(
            name=source["name"],
            address_line_1=source["address_line1"],
            address_line_1_check=source["address_line1_check"],
            address_line_2=source["address_line2"],
            address_city=source["address_city"],
            address_state=source["address_state"],
            address_country=source["address_country"],
            address_zip=source["address_zip"],
            address_zip_check=source["address_zip_check"],
            brand=source["brand"],
            country=source["country"],
            cvc_check=source["cvc_check"],
            dynamic_last4=source["dynamic_last4"],
            tokenization_method=source["tokenization_method"],
            exp_month=source["exp_month"],
            exp_year=source["exp_year"],
            funding=source["funding"],
            last4=source["last4"],
            fingerprint=source["fingerprint"],
        )
        defaults.update({stripe_settings.CUSTOMER_FIELD_NAME: customer})

        card, _ = stripe_settings.CARD_MODEL.objects.update_or_create(
            stripe_id=source["id"], defaults=defaults
        )
        return card

    @classmethod
    def delete(cls, stripe_id):
        """
        Deletes the local card object (Card)
        Args:
            stripe_id: the Stripe ID of the card
        """
        if stripe_id.startswith("card_"):
            return stripe_settings.CARD_MODEL.objects.filter(
                stripe_id=stripe_id
            ).delete()

    @classmethod
    def get_for_customer(cls, customer):
        """
        Returns default source for customer
        Args:
            customer: the customer to get the default source for
        """
        default_card = stripe_settings.CARD_MODEL.objects.filter(
            stripe_id=customer.default_source
        ).first()
        return default_card
