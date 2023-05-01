# Third Party Stuff
import stripe
from django.utils import timezone

# Stripe Integrations Stuff
from stripe_integrations.settings import stripe_settings


class StripeProduct:
    @classmethod
    def sync_all(cls):
        """
        Synchronizes all products from the Stripe API
        """
        products = stripe.Product.auto_paging_iter()
        synced_product_ids = []
        for product in products:
            product_obj, _ = cls.sync(product)
            synced_product_ids.append(product_obj.id)

        # sync deleted products
        stripe_settings.PRODUCT_MODEL.objects.exclude(id__in=synced_product_ids).update(
            date_purged=timezone.now()
        )

    @classmethod
    def sync(cls, product):
        """
        Synchronizes a product from the Stripe API
        Args:
            product: data from Stripe API representing a product
        """
        defaults = {
            "active": product["active"],
            "description": product["description"],
            "metadata": product["metadata"],
            "name": product["name"],
            "statement_descriptor": product["statement_descriptor"],
            "tax_code": product["tax_code"],
            "unit_label": product["unit_label"],
            "images": product["images"],
            "shippable": product["shippable"],
            "package_dimensions": product["package_dimensions"],
            "url": product["url"],
            "livemode": product["livemode"],
            "created": product["created"],
            "updated": product["updated"],
        }

        product, is_created = stripe_settings.PRODUCT_MODEL.objects.update_or_create(
            stripe_id=product["id"], defaults=defaults
        )
        return product, is_created

    @classmethod
    def soft_delete(cls, stripe_id):
        """
        Soft delete the local product object (Product)
        Args:
            stripe_id: the Stripe ID of the product
        """
        if stripe_id.startswith("prod_"):
            product = stripe_settings.PRODUCT_MODEL.objects.filter(
                stripe_id=stripe_id
            ).first()
            if product:
                product.date_purged = timezone.now()
                product.save()
