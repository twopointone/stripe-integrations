# Third Party Stuff
import stripe
from django.utils import timezone

# Stripe Integrations Stuff
from stripe_integrations.actions.products import StripeProduct
from stripe_integrations.settings import stripe_settings


class StripePrice:
    @classmethod
    def sync_all(cls):
        """
        Synchronizes all prices from the Stripe API
        """
        prices = stripe.Price.auto_paging_iter()
        synced_price_ids = []
        for price in prices:
            price_obj, _ = cls.sync(price)
            synced_price_ids.append(price_obj.id)

        # sync deleted prices
        stripe_settings.PRICE_MODEL.objects.exclude(id__in=synced_price_ids).update(
            date_purged=timezone.now()
        )

    @classmethod
    def sync(cls, price):
        """
        Synchronizes a price from the Stripe API
        Args:
            price: data from Stripe API representing a price
        """

        product = stripe_settings.PRODUCT_MODEL.objects.filter(
            stripe_id=price["product"]
        ).first()
        if not product:
            stripe_product = stripe.Product.retrieve(price["product"])
            product, _ = StripeProduct.sync(stripe_product)

        defaults = {
            "active": price["active"],
            "currency": price["currency"],
            "metadata": price["metadata"],
            "nickname": price["nickname"],
            "recurring": price["recurring"],
            "type": price["type"],
            "custom_unit_amount": price["custom_unit_amount"],
            "unit_amount": price["unit_amount"],
            "unit_amount_decimal": price["unit_amount_decimal"],
            "billing_scheme": price["billing_scheme"],
            "tax_behavior": price["tax_behavior"],
            "tiers": price.get("tiers", None),
            "tiers_mode": price["tiers_mode"],
            "transform_quantity": price["transform_quantity"],
            "lookup_key": price["lookup_key"],
            "livemode": price["livemode"],
            "created": price["created"],
            "product": product,
        }

        price, is_created = stripe_settings.PRICE_MODEL.objects.update_or_create(
            stripe_id=price["id"], defaults=defaults
        )
        return price, is_created

    @classmethod
    def soft_delete(cls, stripe_id):
        """
        Soft deletes the local price object (Price)
        Args:
            stripe_id: the Stripe ID of the price
        """
        if stripe_id.startswith("price_"):
            price = stripe_settings.PRICE_MODEL.objects.filter(
                stripe_id=stripe_id
            ).first()
            if price:
                price.date_purged = timezone.now()
                price.save()
