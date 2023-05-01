# Third Party Stuff
import stripe
from django.contrib.postgres.fields import ArrayField, CIEmailField
from django.db import models

# Stripe Integrations Stuff
from stripe_integrations.base.models import StripeObject
from stripe_integrations.utils import CURRENCY_SYMBOLS

USD = "usd"
CURRENCY_CHOICES = ((USD, "USD"),)
DEFAULT_CURRENCY = USD

CHARGE_AUTOMATICALLY = "charge_automatically"
SEND_INVOICE = "send_invoice"

INVOICE_COLLECTION_METHOD_TYPES = (
    (CHARGE_AUTOMATICALLY, "Charge Automatically"),
    (SEND_INVOICE, "Send_Invoice"),
)


class StripeBaseCustomer(StripeObject):
    """
    Customer objects allow us to perform recurring charges and track multiple
    charges that are associated with the same customer
    Stripe documentation: https://stripe.com/docs/api/customers
    """

    EXEMPT = "exempt"
    REVERSE = "reverse"
    NONE = "none"

    TAX_EXEMPT_TYPES = ((EXEMPT, "Exempt"), (REVERSE, "Reverse"), (NONE, "None"))

    # contact details
    name = models.TextField(
        max_length=255,
        blank=True,
        help_text="The customer's full name or business name",
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        help_text="An arbitrary string attached to the object. Often useful for displaying to users.",
    )
    email = CIEmailField(blank=True, db_index=True)
    address = models.JSONField(
        null=True, blank=True, help_text="The customer's address"
    )

    balance = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=True,
        blank=True,
        help_text=(
            "Current balance (in cents), if any, being stored on the customer's "
            "account. "
            "If negative, the customer has credit to apply to the next invoice. "
            "If positive, the customer has an amount owed that will be added to the "
            "next invoice. The balance does not refer to any unpaid invoices; it "
            "solely takes into account amounts that have yet to be successfully "
            "applied to any invoice. This balance is only taken into account for "
            "recurring billing purposes (i.e., subscriptions, invoices, invoice items)"
        ),
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        default=DEFAULT_CURRENCY,
        max_length=3,
        help_text="The currency the customer can be charged in for recurring billing purposes",
    )
    delinquent = models.BooleanField(
        default=False,
        help_text="Whether or not the latest charge for the customer's latest invoice has failed",
    )
    default_source = models.TextField(blank=True)
    shipping = models.JSONField(
        null=True,
        blank=True,
        help_text="Shipping information associated with the customer",
    )
    tax_exempt = models.CharField(
        choices=TAX_EXEMPT_TYPES,
        max_length=16,
        default=NONE,
        help_text="Describes the customer's tax exemption status. When set to reverse, "
        'invoice and receipt PDFs include the text "Reverse charge"',
    )
    preferred_locales = ArrayField(
        models.CharField(default="", blank=True, max_length=255),
        default=[],
        help_text=(
            "The customer's preferred locales (languages), ordered by preference"
        ),
    )

    invoice_prefix = models.CharField(
        default="",
        blank=True,
        max_length=255,
        help_text=(
            "The prefix for the customer used to generate unique invoice numbers"
        ),
    )
    invoice_settings = models.JSONField(
        null=True, blank=True, help_text="The customer's default invoice settings"
    )

    date_purged = models.DateTimeField(null=True, blank=True, editable=False)
    is_active = models.BooleanField(default=True)

    @property
    def stripe_customer(self):
        return stripe.Customer.retrieve(self.stripe_id, expand=["subscriptions"])

    class Meta:
        abstract = True


class StripeBaseCard(StripeObject):
    """
    We can store multiple cards on a customer in order to charge the customer later.
    We can also store multiple debit cards on a recipient in order to transfer to those cards later.
    Stripe documentation: https://stripe.com/docs/api/cards
    """

    name = models.TextField(null=True, blank=True)
    address_line_1 = models.TextField(null=True, blank=True)
    address_line_1_check = models.CharField(null=True, blank=True, max_length=64)
    address_line_2 = models.TextField(null=True, blank=True)
    address_city = models.TextField(null=True, blank=True)
    address_state = models.TextField(null=True, blank=True)
    address_country = models.TextField(null=True, blank=True)
    address_zip = models.TextField(null=True, blank=True)
    address_zip_check = models.CharField(null=True, blank=True, max_length=64)
    brand = models.TextField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=2)
    cvc_check = models.CharField(max_length=32, blank=True, null=True)
    dynamic_last4 = models.CharField(max_length=4, blank=True, null=True)
    tokenization_method = models.CharField(max_length=32, blank=True, null=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(max_length=15, blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    fingerprint = models.TextField(blank=True, null=True)

    def __repr__(self):
        return "Card(pk={!r}, customer={!r})".format(
            self.pk,
            getattr(self, "customer", None),
        )

    class Meta:
        abstract = True


class StripeBaseSubscription(StripeObject):
    """
    Subscriptions allow us to charge a customer on a recurring basis.
    Stripe documentation: https://stripe.com/docs/api/subscriptions
    """

    # https://stripe.com/docs/api/subscriptions/object#subscription_object-status
    INCOMPLETE = "incomplete"  # if the initial payment attempt fails

    # If the first invoice is not paid within 23 hours
    # (Its a terminal status)
    INCOMPLETE_EXPIRED = "incomplete_expired"

    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"  # it becomes past_due when payment to renew it fails

    # 1. it becomes canceled when failed payment is not paid after all retries / by the due date
    # 2. Can be cancelled manually
    #  (Its a terminal status)
    CANCELED = "canceled"

    UNPAID = "unpaid"  # 1. it becomes unpaid When failed payment is not paid after all retries / by the due date

    STATUS_CURRENT = [TRIALING, ACTIVE]
    STATUS_CANCELLED = [CANCELED, UNPAID]

    SUBSCRIPTION_STATUS_TYPES = (
        (INCOMPLETE, "Incomplete"),
        (INCOMPLETE_EXPIRED, "Incomplete Expired"),
        (TRIALING, "Trialing"),
        (ACTIVE, "Active"),
        (PAST_DUE, "Past Due"),
        (CANCELED, "Canceled"),
        (UNPAID, "Unpaid"),
    )

    items = models.JSONField(
        null=True,
        blank=True,
        help_text="List of subscription items, each with an attached price.",
    )
    application_fee_percent = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        help_text="A positive decimal that represents the fee percentage of the "
        "subscription invoice amount that will be transferred to the application "
        "owner's Stripe account each billing period.",
    )
    automatic_tax = models.JSONField(
        null=True,
        blank=True,
        help_text="Automatic tax settings for this subscription.",
    )
    billing_cycle_anchor = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Determines the date of the first full invoice, and, for plans "
            "with `month` or `year` intervals, the day of the month for subsequent "
            "invoices"
        ),
    )
    billing_thresholds = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Define thresholds at which an invoice will be sent, and the subscription advanced to a new billing period"
        ),
    )
    cancel_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="A date in the future at which the subscription will automatically "
        "get canceled",
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text="If the subscription has been canceled with the ``at_period_end`` "
        "flag set to true, ``cancel_at_period_end`` on the subscription will be true. "
        "We can use this attribute to determine whether a subscription that has a "
        "status of active is scheduled to be canceled at the end of the "
        "current period",
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has been canceled, the date of that "
        "cancellation. If the subscription was canceled with ``cancel_at_period_end``, "
        "canceled_at will still reflect the date of the initial cancellation request, "
        "not the end of the subscription period when the subscription is automatically "
        "moved to a canceled state",
    )
    cancellation_details = models.JSONField(
        null=True,
        blank=True,
        help_text=("Details about why this subscription was cancelled"),
    )
    collection_method = models.CharField(
        choices=INVOICE_COLLECTION_METHOD_TYPES,
        max_length=32,
        help_text="Either `charge_automatically`, or `send_invoice`. When charging "
        "automatically, Stripe will attempt to pay this subscription at the end of the "
        "cycle using the default source attached to the customer. "
        "When sending an invoice, Stripe will email us customer an invoice with "
        "payment instructions",
    )
    current_period_end = models.DateTimeField(
        help_text="End of the current period for which the subscription has been "
        "invoiced. At the end of this period, a new invoice will be created"
    )
    current_period_start = models.DateTimeField(
        help_text="Start of the current period for which the subscription has "
        "been invoiced"
    )
    days_until_due = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of days a customer has to pay invoices generated by this "
        "subscription. This value will be `null` for subscriptions where "
        "`billing=charge_automatically`",
    )
    default_payment_method = models.TextField(blank=True)
    default_source = models.TextField(blank=True)

    default_tax_rates = models.JSONField(null=True, blank=True)
    discount = models.JSONField(null=True, blank=True)
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has ended (either because it was canceled or "
        "because the customer was switched to a subscription to a new plan), "
        "the date the subscription ended",
    )
    next_pending_invoice_item_invoice = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Specifies the approximate timestamp on which any pending "
        "invoice items will be billed according to the schedule provided at "
        "pending_invoice_item_interval",
    )
    pause_collection = models.JSONField(
        null=True,
        blank=True,
        help_text="If specified, payment collection for this subscription will be paused.",
    )
    pending_invoice_item_interval = models.JSONField(
        null=True,
        blank=True,
        help_text="Specifies an interval for how often to bill for any "
        "pending invoice items. It is analogous to calling Create an invoice "
        "for the given subscription at the specified interval",
    )
    pending_setup_intent = models.TextField(blank=True)
    pending_update = models.JSONField(
        null=True,
        blank=True,
        help_text="If specified, pending updates that will be applied to the "
        "subscription once the latest_invoice has been paid",
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
        help_text="The quantity applied to this subscription. This value will be "
        "`null` for multi-plan subscriptions",
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the subscription was first created. The date "
        "might differ from the created date due to backdating",
    )
    status = models.CharField(
        choices=SUBSCRIPTION_STATUS_TYPES,
        max_length=32,
        help_text="The status of this subscription",
    )

    # tax rate
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has a trial, the end of that trial",
    )
    trial_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has a trial, the beginning of that trial",
    )
    trial_settings = models.JSONField(
        null=True,
        blank=True,
        help_text="Settings related to subscription trials.",
    )
    latest_invoice = models.CharField(
        max_length=255,
        blank=True,
        help_text="The most recent invoice this subscription has generated.",
    )

    @property
    def stripe_subscription(self):
        return stripe.Subscription.retrieve(self.stripe_id)

    class Meta:
        abstract = True


class StripeBaseEvent(StripeObject):
    kind = models.CharField(max_length=255)
    webhook_message = models.JSONField()
    validated_message = models.JSONField(null=True, blank=True)
    valid = models.BooleanField(null=True)
    processed = models.BooleanField(default=False)
    request = models.JSONField(
        null=True,
        help_text="Information on the API request that instigated the event, If null, the event was automatic"
        " (e.g., Stripe’s automatic subscription handling)",
    )
    pending_webhooks = models.PositiveIntegerField(
        default=0,
        help_text="Number of webhooks that have yet to be successfully "
        "delivered (i.e., to return a 20x response) "
        "to the URLs we’ve specified",
    )
    api_version = models.CharField(max_length=128, blank=True)

    @property
    def message(self):
        return self.validated_message

    def __str__(self):
        return "{} - {}".format(self.kind, self.stripe_id)

    class Meta:
        abstract = True


class StripeBaseCoupon(StripeObject):
    """
    A coupon contains information about a percent-off or amount-off discount we might want to apply to a customer.
    Coupons may be applied to invoices or orders. Coupons do not work with conventional one-off charges.
    Stripe documentation: https://stripe.com/docs/api/coupons
    """

    ONCE = "once"
    REPEATING = "repeating"
    FOREVER = "forever"

    STRIPE_COUPON_DURATION_TYPES = (
        (ONCE, "Once"),
        (REPEATING, "Repeating"),
        (FOREVER, "Forever"),
    )

    name = models.CharField(
        max_length=64,
        blank=True,
        help_text="Name of the coupon displayed to customers on for instance invoices or receipts",
    )
    applies_to = models.JSONField(
        null=True,
        blank=True,
        help_text="Contains information about what product this coupon applies to. This field is not included by default. "
        "To include it in the response, expand the applies_to field",
    )
    amount_off = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=True,
        blank=True,
        help_text="Amount (in the currency specified) "
        "that will be taken off the subtotal "
        "of any invoices for this customer",
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        default=DEFAULT_CURRENCY,
        max_length=3,
        help_text="If amount_off has been set, the three-letter ISO code for the currency of the amount to take off",
    )
    duration = models.CharField(
        choices=STRIPE_COUPON_DURATION_TYPES,
        max_length=16,
        default="once",
        help_text="One of forever, once, and repeating. "
        "Describes how long a customer who applies this coupon "
        "will get the discount",
    )
    duration_in_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Required only if duration is repeating, in which case it must be a positive integer that "
        "specifies the number of months the discount will be in effect",
    )
    max_redemptions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="A positive integer specifying the number of times the coupon can "
        "be redeemed before it’s no longer valid",
    )
    percent_off = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Percent that will be taken off the subtotal of any invoices "
        "for this customer for the duration of the coupon",
    )
    redeem_by = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date after which the coupon can no longer be redeemed",
    )
    times_redeemed = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of times this coupon has been applied to a customer",
    )

    valid = models.BooleanField(default=False)

    # Soft delete price in DB on deletion from stripe
    date_purged = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        if self.amount_off is None:
            description = "{}% off".format(
                self.percent_off,
            )
        else:
            description = "{}{}".format(
                CURRENCY_SYMBOLS.get(self.currency, ""), self.amount_off
            )

        return "Coupon for {}, {}".format(description, self.duration)

    class Meta:
        abstract = True


class StripeBaseProduct(StripeObject):
    """
    Products describe the specific goods or services you offer to your customers.
    For example, you might offer a Standard and Premium version of your goods or service;
    each version would be a separate Product. They can be used in conjunction with Prices
    to configure pricing in Payment Links, Checkout, and Subscriptions.
    Stripe documentation: https://stripe.com/docs/api/products
    """

    active = models.BooleanField(
        help_text=("Whether the product is currently available for purchase."),
    )
    description = models.TextField(
        null=True,
        help_text="The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.",
    )
    name = models.CharField(
        max_length=255,
        help_text="The product’s name, meant to be displayable to the customer. Whenever this product is sold via a subscription, name will show up on associated invoice line item descriptions.",
    )

    statement_descriptor = models.TextField(
        null=True,
        help_text=(
            "Extra information about a product which will appear on your customer’s credit card statement."
            "In the case that multiple products are billed at once, the first statement descriptor will be used."
        ),
    )
    tax_code = models.CharField(max_length=255, null=True, help_text="A tax code ID.")
    unit_label = models.CharField(
        max_length=255,
        null=True,
        help_text=(
            "A label that represents units of this product in Stripe and on customers’ receipts and invoices."
            "When set, this will be included in associated invoice line item descriptions."
        ),
    )
    images = ArrayField(
        models.CharField(max_length=255),
        size=8,
        default=list,
        help_text=(
            "A list of up to 8 URLs of images for this product, meant to be displayable to the customer."
        ),
    )
    shippable = models.BooleanField(
        null=True, help_text="Whether this product is shipped (i.e., physical goods)."
    )
    package_dimensions = models.JSONField(
        null=True,
        help_text="The dimensions of this product for shipping purposes.",
    )
    url = models.URLField(
        max_length=500,
        null=True,
        help_text="A URL of a publicly-accessible webpage for this product.",
    )
    created = models.BigIntegerField(
        help_text="Time at which the object was created. Measured in seconds since the Unix epoch"
    )
    updated = models.BigIntegerField(
        help_text="Time at which the object was last updated. Measured in seconds since the Unix epoch"
    )

    # Soft delete product in DB on deletion from stripe
    date_purged = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True


class StripeBasePrice(StripeObject):
    """
    Prices define the unit cost, currency, and (optional) billing cycle for both
    recurring and one-time purchases of products. Products help you track inventory
    or provisioning, and prices help you track payment terms. Different physical
    goods or levels of service should be represented by products, and pricing options
    should be represented by prices. This approach lets you change prices without
    having to change your provisioning scheme.

    For example, you might have a single "gold" product that has prices for $10/month, $100/year, and €9 once.
    Stripe documentation: https://stripe.com/docs/api/prices
    """

    ONE_TIME = "one_time"
    RECURRING = "recurring"

    PRICE_TYPES = [
        (ONE_TIME, "One Time"),
        (RECURRING, "Recurring"),
    ]

    TAX_INCLUSIVE = "inclusive"
    TAX_EXCLUSIVE = "exclusive"
    TAX_UNSPECIFIED = "unspecified"

    TAX_BEHAVIOR_TYPES = [
        (TAX_INCLUSIVE, "TAX Inclusive"),
        (TAX_EXCLUSIVE, "TAX Exclusive"),
        (TAX_INCLUSIVE, "TAX Unspecified"),
    ]

    PER_UNIT = "per_unit"
    TIERED = "tiered"

    BILLING_SCHEME_TYPES = [
        (PER_UNIT, "Per Unit"),
        (TIERED, "Tiered"),
    ]

    active = models.BooleanField(
        help_text="Whether the price can be used for new purchases."
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=3,
        help_text="Three-letter ISO currency code, in lowercase. Must be a supported currency.",
    )
    nickname = models.CharField(
        max_length=255,
        null=True,
        help_text="A brief description of the price, hidden from customers.",
    )
    recurring = models.JSONField(
        null=True,
        help_text="The recurring components of a price such as interval and usage_type.",
    )

    type = models.CharField(
        choices=PRICE_TYPES,
        max_length=16,
        help_text=(
            "One of one_time or recurring depending on whether the price is for "
            "a one-time purchase or a recurring (subscription) purchase."
        ),
    )
    custom_unit_amount = models.JSONField(
        null=True,
        help_text=(
            "When set, provides configuration for the amount to be adjusted "
            "by the customer during Checkout Sessions and Payment Links."
        ),
    )
    unit_amount = models.BigIntegerField(
        null=True,
        help_text=(
            "The unit amount in cents to be charged, represented as a whole "
            "integer if possible. Null if a sub-cent precision is required"
        ),
    )
    unit_amount_decimal = models.DecimalField(
        null=True,
        max_digits=19,
        decimal_places=12,
        help_text=(
            "The unit amount in cents to be charged, represented as a decimal "
            "string with at most 12 decimal places"
        ),
    )
    billing_scheme = models.CharField(
        choices=BILLING_SCHEME_TYPES,
        max_length=16,
        help_text=(
            "Describes how to compute the price per period. Either per_unit or tiered."
            "per_unit indicates that the fixed amount (specified in unit_amount or unit_amount_decimal)"
            "will be charged per unit in quantity (for prices with usage_type=licensed),"
            "or per unit of total usage (for prices with usage_type=metered). tiered indicates that the unit"
            "pricing will be computed using a tiering strategy as defined using the tiers and tiers_mode attributes."
        ),
    )

    tax_behavior = models.CharField(
        choices=TAX_BEHAVIOR_TYPES,
        max_length=16,
        help_text=(
            "Specifies whether the price is considered inclusive of taxes or exclusive of taxes."
            "One of inclusive, exclusive, or unspecified. Once specified as either inclusive or exclusive, it cannot be changed."
        ),
    )
    tiers = models.JSONField(
        null=True,
        help_text=(
            "Each element represents a pricing tier. This parameter requires billing_scheme to be set to tiered."
            "See also the documentation for billing_scheme. This field is not included by default."
            "To include it in the response, expand the tiers field."
        ),
    )
    tiers_mode = models.CharField(
        null=True,
        max_length=32,
        help_text=(
            "Defines if the tiering price should be graduated or volume based."
            "In volume-based tiering, the maximum quantity within a period determines the per unit price."
            "In graduated tiering, pricing can change as the quantity grows."
        ),
    )
    transform_quantity = models.JSONField(
        null=True,
        help_text=(
            "Apply a transformation to the reported usage or set quantity before computing the amount billed. Cannot be combined with tiers."
        ),
    )
    lookup_key = models.CharField(
        null=True,
        max_length=255,
        help_text="A lookup key used to retrieve prices dynamically from a static string. This may be up to 200 characters.",
    )
    created = models.BigIntegerField(
        help_text="Time at which the object was created. Measured in seconds since the Unix epoch"
    )

    # Soft delete price in DB on deletion from stripe
    date_purged = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True
