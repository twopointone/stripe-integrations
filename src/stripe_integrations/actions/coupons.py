# Third Party Stuff
import stripe
from django.utils import timezone

# Stripe Integrations Stuff
from stripe_integrations import utils
from stripe_integrations.settings import stripe_settings


class StripeCoupon:
    @classmethod
    def sync(cls, stripe_coupon):
        """
        Sync stripe coupons data
        Note:
            applies_to: This key is not received from stripe
            when the coupon is not applied to specific product
        Args:
            stripe_coupon: Stripe coupon object
        Retruns:
            coupon object, is_created status (Boolean)
        """
        defaults = dict(
            amount_off=(
                utils.convert_amount_for_db(
                    stripe_coupon["amount_off"], stripe_coupon["currency"]
                )
                if stripe_coupon["amount_off"]
                else None
            ),
            currency=stripe_coupon["currency"] or "",
            duration=stripe_coupon["duration"],
            duration_in_months=stripe_coupon["duration_in_months"],
            max_redemptions=stripe_coupon["max_redemptions"],
            metadata=stripe_coupon["metadata"],
            name=stripe_coupon["name"],
            applies_to=stripe_coupon.get("applies_to", None),
            percent_off=stripe_coupon["percent_off"],
            redeem_by=utils.convert_tstamp(stripe_coupon["redeem_by"])
            if stripe_coupon["redeem_by"]
            else None,
            times_redeemed=stripe_coupon["times_redeemed"],
            valid=stripe_coupon["valid"],
            livemode=stripe_coupon["livemode"],
        )

        coupon, is_created = stripe_settings.COUPON_MODEL.objects.update_or_create(
            stripe_id=stripe_coupon["id"], defaults=defaults
        )
        return coupon, is_created

    @classmethod
    def sync_all(cls):
        """
        Synchronizes all coupons from the Stripe API
        Retruns:
            list of coupons that is synced
        """
        strip_coupons = stripe.Coupon.auto_paging_iter(expand=["data.applies_to"])
        coupons = []

        for coupon in strip_coupons:
            obj, _ = cls.sync(coupon)
            coupons.append(obj)

        return coupons

    @classmethod
    def get(cls, stripe_id):
        """
        Retrieve coupon object
        Args:
            stripe_id: Coupon's stripe id
        Retruns:
            a coupon object
        """
        coupon = stripe_settings.COUPON_MODEL.objects.filter(
            stripe_id=stripe_id, valid=True
        ).first()
        return coupon

    @classmethod
    def soft_delete(cls, stripe_id):
        """
        Deletes the local price object (Coupon)
        Args:
            stripe_id: the Stripe ID of the coupon
        """
        coupon = stripe_settings.COUPON_MODEL.objects.filter(
            stripe_id=stripe_id
        ).first()
        if coupon:
            coupon.date_purged = timezone.now()
            coupon.save()
