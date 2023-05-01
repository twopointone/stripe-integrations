# Models

A set of base abstract models is included in the library, which encompasses all standard Stripe object fields.
This means that developers can inherit these models to incorporate Stripe functionality into their Django projects and add any necessary custom fields.

## Customer

A customer represents an individual or entity that engages with your business. To create a customer model that incorporates all the fields found in a Stripe customer object, developers can inherit from `StripeBaseCustomer` provided by the library.

!!! Example
    ```python
    from django.db import models

    from stripe_integrations.models import StripeBaseCustomer
    from users.models import User


    class Customer(StripeBaseCustomer):
        user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name="stripe_customers",
        )
    ```

### Fields

The `StripeBaseCustomer` abstract model provides the following fields:

| Parameter                                   | Description                                                                                                                                                                                                                                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| id (string)                                 | The primary key id (uuid) of the customer in the local database.                                                                                                                                                                                                                     |
| created_at (datetime)                       | Timestamp when the customer object was created in the local database.                                                                                                                                                                                                                |
| updated_at (datetime)                       | Timestamp when the customer object was last updated in the local database.                                                                                                                                                                                                           |
| stripe_id (string)                          | Customer's stripe id                                                                                                                                                                                                                                                                 |
| name (string)                               | The customer’s full name or business name.                                                                                                                                                                                                                                           |
| description (string)                        | An arbitrary string attached to the object. Often useful for displaying to users.                                                                                                                                                                                                    |
| email (string)                              | The customer’s email address.                                                                                                                                                                                                                                                        |
| address (string)                            | The customer’s address.                                                                                                                                                                                                                                                              |
| balance (integer)                           | An integer amount in cents that represents the customer’s current balance, which affect the customer’s future invoices. A negative amount represents a credit that decreases the amount due on an invoice; a positive amount increases the amount due on an invoice.                 |
| currency (string)                           | Three-letter [ISO code for the currency](https://stripe.com/docs/currencies) the customer can be charged in for recurring billing purposes. <br>Choices: "usd"                                                                                                                       |
| delinquent (boolean)                        | When the customer’s latest invoice is billed by charging automatically, delinquent is true if the invoice’s latest charge failed. When the customer’s latest invoice is billed by sending an invoice, delinquent is true if the invoice isn’t paid by its due date.                  |
| default_source (string)                     | ID of the default payment source for the customer.                                                                                                                                                                                                                                   |
| shipping (json)                             | Mailing and shipping address for the customer. Appears on invoices emailed to this customer.                                                                                                                                                                                         |
| tax_exempt (string)                         | Describes the customer’s tax exemption status. One of `none`, `exempt`, or `reverse`. When set to reverse, invoice and receipt PDFs include the text "Reverse charge".                                                                                                               |
| preferred_locales (array containing string) | The customer’s preferred locales (languages), ordered by preference.                                                                                                                                                                                                                 |
| invoice_prefix (string)                     | The prefix for the customer used to generate unique invoice numbers. Must be 3–12 uppercase letters or numbers.                                                                                                                                                                      |
| invoice_settings (json)                     | Default invoice settings for this customer.                                                                                                                                                                                                                                          |
| livemode (boolean)                          | Has the value `true` if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                         |
| date_purged (datetime)                      | Deleted at datetime by which we can determine when the customer was deleted. When a customer is deleted on stripe this field will be updated.                                                                                                                                        |
| is_active (boolean)                         | Determine customer is active or not                                                                                                                                                                                                                                                  |
| metadata (json)                             | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. |
| livemode (boolean)                          | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                           |


### Configuration

Once the `Customer` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "CUSTOMER_MODEL": "app.models.Customer",
    "USER_FIELD_NAME": "user",
}
```

## Card

In the context of payment processing, a card refers to the payment method that a customer will use to make a payment. To define a card model that includes all the fields found in a Stripe card object, developers can inherit from `StripeBaseCard` provided by the library.

!!! Example
    ```python
    from django.db import models

    from stripe_integrations.models import StripeBaseCard


    class Card(StripeBaseCard):
        customer = models.ForeignKey(
            Customer,
            on_delete=models.CASCADE,
            related_name="cards",
        )
    ```

### Fields

The `StripeBaseCard` abstract model provides the following fields:

| Parameter                     | Description                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id (string)                   | The primary key id (uuid) of the card in the local database.                                                                                                                                                                                                                                                                                |
| created_at (datetime)         | Timestamp when the card object was created in the local database.                                                                                                                                                                                                                                                                           |
| updated_at (datetime)         | Timestamp when the card object was last updated in the local database.                                                                                                                                                                                                                                                                      |
| stripe_id (string)            | Customer's stripe id                                                                                                                                                                                                                                                                                                                        |
| name (string)                 | Cardholder name.                                                                                                                                                                                                                                                                                                                            |
| address_line_1 (string)       | Address line 1 (Street address/PO Box/Company name).                                                                                                                                                                                                                                                                                        |
| address_line_1_check (string) | If address_line1 was provided, results of the check: pass, fail, unavailable, or unchecked.                                                                                                                                                                                                                                                 |
| address_line_2 (string)       | Address line 2 (Apartment/Suite/Unit/Building).                                                                                                                                                                                                                                                                                             |
| address_city (string)         | City/District/Suburb/Town/Village.                                                                                                                                                                                                                                                                                                          |
| address_state (string)        | State/County/Province/Region.                                                                                                                                                                                                                                                                                                               |
| address_country (string)      | Billing address country, if provided when creating card.                                                                                                                                                                                                                                                                                    |
| address_zip (string)          | ZIP or postal code.                                                                                                                                                                                                                                                                                                                         |
| address_zip_check (string)    | If address_zip was provided, results of the check: `pass`, `fail`, `unavailable`, or `unchecked`.                                                                                                                                                                                                                                           |
| brand (string)                | Card brand. Can be `American Express`, `Diners Club`, `Discover, JCB`, `MasterCard`, `UnionPay`, `Visa`, or `Unknown`.                                                                                                                                                                                                                      |
| country (string)              | Two-letter ISO code representing the country of the card. You could use this attribute to get a sense of the international breakdown of cards you’ve collected.                                                                                                                                                                             |
| cvc_check (string)            | If a CVC was provided, results of the check: `pass`, `fail`, `unavailable`, or `unchecked`. A result of `unchecked` indicates that CVC was provided but hasn’t been checked yet. Checks are typically performed when attaching a card to a Customer object, or when creating a charge.                                                      |
| dynamic_last4 (string)        | (For tokenized numbers only.) The last four digits of the device account number.                                                                                                                                                                                                                                                            |
| tokenization_method (string)  | If the card number is tokenized, this is the method that was used. Can be `android_pay` (includes Google Pay), `apple_pay`, `masterpass`, `visa_checkout`, or null.                                                                                                                                                                         |
| exp_month (integer)           | Two-digit number representing the card’s expiration month.                                                                                                                                                                                                                                                                                  |
| exp_year (integer)            | Four-digit number representing the card’s expiration year.                                                                                                                                                                                                                                                                                  |
| funding (string)              | Card funding type. Can be `credit`, `debit`, `prepaid`, or `unknown`.                                                                                                                                                                                                                                                                       |
| last4 (string)                | The last four digits of the card.                                                                                                                                                                                                                                                                                                           |
| fingerprint (string)          | Uniquely identifies this particular card number. You can use this attribute to check whether two customers who’ve signed up with you are using the same card number, for example. For payment methods that tokenize card information (Apple Pay, Google Pay), the tokenized number might be provided instead of the underlying card number. |
| metadata (json)               | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.                                                        |
| livemode (boolean)            | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                                                                                  |


### Configuration

Once the `Card` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "CARD_MODEL": "app.models.Card",
    "CUSTOMER_FIELD_NAME": "customer",
}
```

## Subscription

Subscriptions enable businesses to charge customers on a recurring basis. To define a subscription model that incorporates all the fields found in a Stripe subscription object, developers can inherit from `StripeBaseSubscription` provided by the library.

!!! Example
    ```python
    from django.db import models

    from stripe_integrations.models import StripeBaseSubscription


    class Subscription(StripeBaseSubscription):
        customer = models.ForeignKey(
            Customer,
            on_delete=models.CASCADE,
            related_name="subscriptions",
            help_text="The customer associated with this subscription",
        )
    ```

### Fields

The `StripeBaseSubscription` abstract model provides the following fields:

| Field                                        | Description                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id (string)                                  | The primary key id (uuid) of the subscription in the local database.                                                                                                                                                                                                                                                                  |
| created_at (datetime)                        | Timestamp when the subscription object was created in the local database.                                                                                                                                                                                                                                                             |
| updated_at (datetime)                        | Timestamp when the subscription object was last updated in the local database.                                                                                                                                                                                                                                                        |
| stripe_id (string)                           | Customer's stripe id                                                                                                                                                                                                                                                                                                                  |
| items (json)                                 | List of subscription items, each with an attached price.                                                                                                                                                                                                                                                                              |
| application_fee_percent (decimal)            | A non-negative decimal between 0 and 100, with at most two decimal places. This represents the percentage of the subscription invoice subtotal that will be transferred to the application owner’s Stripe account.                                                                                                                    |
| automatic_tax (json)                         | Automatic tax settings for this subscription.                                                                                                                                                                                                                                                                                         |
| billing_cycle_anchor (datetime)              | Determines the date of the first full invoice, and, for plans with `month` or `year` intervals, the day of the month for subsequent invoices. The timestamp is in UTC format.                                                                                                                                                         |
| billing_thresholds (json)                    | Define thresholds at which an invoice will be sent, and the subscription advanced to a new billing period                                                                                                                                                                                                                             |
| cancel_at (datetime)                         | A date in the future at which the subscription will automatically get canceled                                                                                                                                                                                                                                                        |
| cancel_at_period_end (boolean)               | If the subscription has been canceled with the `at_period_end` flag set to true, `cancel_at_period_end` on the subscription will be true. You can use this attribute to determine whether a subscription that has a status of active is scheduled to be canceled at the end of the current period.                                    |
| canceled_at (datetime)                       | If the subscription has been canceled, the date of that cancellation. If the subscription was canceled with `cancel_at_period_end`, `canceled_at` will reflect the time of the most recent update request, not the end of the subscription period when the subscription is automatically moved to a canceled state.                   |
| cancellation_details (json)                  | Details about why this subscription was cancelled                                                                                                                                                                                                                                                                                     |
| collection_method (string)                   | Either charge_automatically, or send_invoice. When charging automatically, Stripe will attempt to pay this subscription at the end of the cycle using the default source attached to the customer. When sending an invoice, Stripe will email your customer an invoice with payment instructions and mark the subscription as active. |
| current_period_end (datetime)                | End of the current period that the subscription has been invoiced for. At the end of this period, a new invoice will be created.                                                                                                                                                                                                      |
| current_period_start (datetime)              | Start of the current period that the subscription has been invoiced for.                                                                                                                                                                                                                                                              |
| days_until_due (integer)                     | Details about why this subscription was cancelled                                                                                                                                                                                                                                                                                     |
| default_payment_method (string)              | ID of the default payment method for the subscription. It must belong to the customer associated with the subscription. This takes precedence over default_source.                                                                                                                                                                    |
| default_source (string)                      | ID of the default payment source for the subscription. It must belong to the customer associated with the subscription and be in a chargeable state. If `default_payment_method` is also set, `default_payment_method` will take precedence.                                                                                          |
| default_tax_rates (json)                     | The tax rates that will apply to any subscription item that does not have `tax_rates` set. Invoices created will have their `default_tax_rates` populated from the subscription.                                                                                                                                                      |
| discount (json)                              | Describes the current discount applied to this subscription, if there is one. When billing, a discount applied to a subscription overrides a discount applied on a customer-wide basis.                                                                                                                                               |
| ended_at (datetime)                          | If the subscription has ended, the date the subscription ended.                                                                                                                                                                                                                                                                       |
| next_pending_invoice_item_invoice (datetime) | Specifies the approximate timestamp on which any pending invoice items will be billed according to the schedule provided at `pending_invoice_item_interval`.                                                                                                                                                                          |
| pause_collection (json)                      | If specified, payment collection for this subscription will be paused.                                                                                                                                                                                                                                                                |
| pending_invoice_item_interval (json)         | Specifies an interval for how often to bill for any pending invoice items. It is analogous to calling Create an invoice for the given subscription at the specified interval.                                                                                                                                                         |
| pending_setup_intent (string)                | You can use this SetupIntent to collect user authentication when creating a subscription without immediate payment or updating a subscription’s payment method, allowing you to optimize for off-session payments. Learn more in the SCA Migration Guide.                                                                             |
| pending_update (json)                        | If specified, pending updates that will be applied to the subscription once the `latest_invoice` has been paid.                                                                                                                                                                                                                       |
| quantity (integer)                           | The quantity applied to this subscription. This value will be `null` for multi-plan subscriptions                                                                                                                                                                                                                                     |
| start_date (datetime)                        | Date when the subscription was first created. The date might differ from the `created` date due to backdating.                                                                                                                                                                                                                        |
| status (string)                              | The status of this subscription. Possible values are `incomplete`, `incomplete_expired`, `trialing`, `active`, `past_due`, `canceled`, or `unpaid`.                                                                                                                                                                                   |
| trial_end (datetime)                         | If the subscription has a trial, the end of that trial.                                                                                                                                                                                                                                                                               |
| trial_start (datetime)                       | If the subscription has a trial, the beginning of that trial.                                                                                                                                                                                                                                                                         |
| trial_settings (json)                        | Settings related to subscription trials.                                                                                                                                                                                                                                                                                              |
| latest_invoice (string)                      | The most recent invoice this subscription has generated.                                                                                                                                                                                                                                                                              |
| metadata (json)                              | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.                                                  |
| livemode (boolean)                           | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                                                                            |

### Configuration

Once the `Card` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "SUBSCRIPTION_MODEL": "app.models.Subscription",
    "CUSTOMER_FIELD_NAME": "customer",
}
```

## Product

In the context of payment processing, a product refers to a specific good or service offered to customers. For instance, a business might offer both a standard and premium version of a product, with each version being a distinct product. Products can be used with Prices to configure pricing in Payment Links, Checkout, and Subscriptions. To define a product model that incorporates all the fields found in a Stripe product object, developers can inherit from `StripeBaseProduct` provided by the library.

!!! Example
    ```python
    from stripe_integrations.models import StripeBaseProduct


    class Product(StripeBaseProduct):
        pass
    ```

### Fields

The `StripeBaseProduct` abstract model provides the following fields:

| Field                             | Description                                                                                                                                                                                                                                                                          |
| --------------------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id (string)                       | The primary key id (uuid) of the product in the local database.                                                                                                                                                                                                                      |
| created_at (datetime)             | Timestamp when the product object was created in the local database.                                                                                                                                                                                                                 |
| updated_at (datetime)             | Timestamp when the product object was last updated in the local database.                                                                                                                                                                                                            |
| stripe_id (string)                | Stripe object id                                                                                                                                                                                                                                                                     |
| active (boolean)                  | Whether the product is currently available for purchase.                                                                                                                                                                                                                             |
| description (string)              | The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.                                                                                            |
| name (string)                     | The product’s name, meant to be displayable to the customer. Whenever this product is sold via a subscription, name will show up on associated invoice line item descriptions.                                                                                                       |
| statement_descriptor (string)     | Extra information about a product which will appear on your customer’s credit card statement. In the case that multiple products are billed at once, the first statement descriptor will be used.                                                                                    |
| tax_code (string)                 | A [tax code](https://stripe.com/docs/tax/tax-categories) ID.                                                                                                                                                                                                                         |
| unit_label (string)               | A label that represents units of this product. When set, this will be included in customers’ receipts, invoices, Checkout, and the customer portal.                                                                                                                                  |
| images (array containing strings) | A list of up to 8 URLs of images for this product, meant to be displayable to the customer.                                                                                                                                                                                          |
| shippable (boolean)               | Whether this product is shipped (i.e., physical goods).                                                                                                                                                                                                                              |
| package_dimensions (json)         | The dimensions of this product for shipping purposes.                                                                                                                                                                                                                                |
| url (string)                      | A URL of a publicly-accessible webpage for this product.                                                                                                                                                                                                                             |
| created (integer)                 | Time at which the object was created. Measured in seconds since the Unix epoch                                                                                                                                                                                                       |
| updated (integer)                 | Time at which the object was last updated. Measured in seconds since the Unix epoch.                                                                                                                                                                                                 |
| date_purged (datetime)            | Deleted at datetime by which we can determine when the product was deleted. When a product is deleted on stripe this field will be updated.                                                                                                                                          |
| metadata (json)                   | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. |
| livemode (boolean)                | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                           |

### Configuration

Once the `Product` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "PRODUCT_MODEL": "app.models.Product"
}
```

## Price

Prices define the cost per unit, currency, and billing cycle (if applicable) for both recurring and one-time purchases of products. Products are used to track inventory or provisioning, while prices are used to track payment terms. By representing different physical goods or levels of service as products and pricing options as prices, businesses can modify prices without changing their provisioning scheme. To define a price model that incorporates all the fields found in a Stripe price object, developers can inherit from `StripeBasePrice` provided by the library.

!!! Example
    ```python
    from stripe_integrations.models import StripeBasePrice


    class Price(StripeBasePrice):
        product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            related_name="prices",
        )
    ```

### Fields

The `StripeBasePrice` abstract model provides the following fields:

| Field                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id (string)                   | The primary key id (uuid) of the price in the local database.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| created_at (datetime)         | Timestamp when the price object was created in the local database.                                                                                                                                                                                                                                                                                                                                                                                                             |
| updated_at (datetime)         | Timestamp when the price object was last updated in the local database.                                                                                                                                                                                                                                                                                                                                                                                                        |
| stripe_id (string)            | Stripe object id                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| active (boolean)              | Whether the price can be used for new purchases.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| currency (string)             | Three-letter ISO currency code, in lowercase. Must be a supported currency. <br> Choices: "usd"                                                                                                                                                                                                                                                                                                                                                                                |
| nickname (string)             | A brief description of the price, hidden from customers.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| recurring (string)            | The recurring components of a price such as `interval` and `usage_type`.                                                                                                                                                                                                                                                                                                                                                                                                       |
| tax_code (string)             | A [tax code](https://stripe.com/docs/tax/tax-categories) ID.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| type (string)                 | One of `one_time` or `recurring` depending on whether the price is for a one-time purchase or a recurring (subscription) purchase.                                                                                                                                                                                                                                                                                                                                             |
| custom_unit_amount (json)     | When set, provides configuration for the amount to be adjusted by the customer during Checkout Sessions and Payment Links.                                                                                                                                                                                                                                                                                                                                                     |
| unit_amount (integer)         | The unit amount in cents to be charged, represented as a whole integer if possible. Only set if `billing_scheme=per_unit`.                                                                                                                                                                                                                                                                                                                                                     |
| unit_amount_decimal (decimal) | The unit amount in cents to be charged, represented as a decimal string with at most 12 decimal places. Only set if `billing_scheme=per_unit`.                                                                                                                                                                                                                                                                                                                                 |
| billing_scheme (string)       | Describes how to compute the price per period. Either `per_unit` or `tiered`. `per_unit` indicates that the fixed amount (specified in `unit_amount` or `unit_amount_decimal`) will be charged per unit in `quantity` (for prices with `usage_type=licensed`), or per unit of total usage (for prices with `usage_type=metered`). `tiered` indicates that the unit pricing will be computed using a tiering strategy as defined using the `tiers` and `tiers_mode` attributes. |
| created (int)                 | Time at which the object was created. Measured in seconds since the Unix epoch                                                                                                                                                                                                                                                                                                                                                                                                 |
| tax_behavior (string)         | Specifies whether the price is considered inclusive of taxes or exclusive of taxes. One of `inclusive`, `exclusive`, or `unspecified`. Once specified as either `inclusive` or `exclusive`, it cannot be changed.                                                                                                                                                                                                                                                              |
| tiers (json)                  | Each element represents a pricing tier. This parameter requires `billing_scheme` to be set to `tiered`. See also the documentation for `billing_scheme`.                                                                                                                                                                                                                                                                                                                       |
| tiers_mode (string)           | Defines if the tiering price should be `graduated` or `volume` based. In volume-based tiering, the maximum quantity within a period determines the per unit price. In `graduated` tiering, pricing can change as the quantity grows.                                                                                                                                                                                                                                           |
| transform_quantity (json)     | Apply a transformation to the reported usage or set quantity before computing the amount billed. Cannot be combined with `tiers`.                                                                                                                                                                                                                                                                                                                                              |
| created (integer)             | Time at which the object was created. Measured in seconds since the Unix epoch.                                                                                                                                                                                                                                                                                                                                                                                                |
| lookup_key (string)           | A lookup key used to retrieve prices dynamically from a static string. This may be up to 200 characters.                                                                                                                                                                                                                                                                                                                                                                       |
| date_purged (datetime)        | Deleted at datetime by which we can determine when the price was deleted. When a price is deleted on stripe this field will be updated.                                                                                                                                                                                                                                                                                                                                        |
| metadata (json)               | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.                                                                                                                                                                                           |
| livemode (boolean)            | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                                                                                                                                                                                                                     |

### Configuration

Once the `Price` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "PRICE_MODEL": "app.models.Price"
}
```

## Coupon

Coupons contain information about discounts in the form of percentage or fixed amount that businesses can apply to a customer's purchase. These coupons can be used for various purposes, such as for subscriptions, invoices, checkout sessions, and quotes. However, they cannot be used with conventional one-off charges or payment intents. To define a coupon model that incorporates all the fields found in a Stripe coupon object, developers can inherit from `StripeBaseCoupon` provided by the library.

!!! Example
    ```python
    from stripe_integrations.models import StripeBaseCoupon


    class Coupon(StripeBaseCoupon):
        pass
    ```

### Fields

The `StripeBaseCoupon` abstract model provides the following fields:

| Field                        | Description                                                                                                                                                                                                                                                                          |
| ---------------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id (string)                  | The primary key id (uuid) of the coupon in the local database.                                                                                                                                                                                                                       |
| created_at (datetime)        | Timestamp when the coupon object was created in the local database.                                                                                                                                                                                                                  |
| updated_at (datetime)        | Timestamp when the coupon object was last updated in the local database.                                                                                                                                                                                                             |
| stripe_id (string)           | Stripe object id                                                                                                                                                                                                                                                                     |
| name (string)                | Name of the coupon displayed to customers on for instance invoices or receipts.                                                                                                                                                                                                      |
| applies_to (json)            | Contains information about what this coupon applies to.                                                                                                                                                                                                                              |
| amount_off (decimal)         | Amount (in the `currency` specified) that will be taken off the subtotal of any invoices for this customer.                                                                                                                                                                          |
| currency (string)            | If amount_off has been set, the three-letter [ISO code for the currency](https://stripe.com/docs/currencies) of the amount to take off. <br>Choice: `usd`                                                                                                                            |
| duration (string)            | One of `forever`, `once`, and `repeating`. Describes how long a customer who applies this coupon will get the discount.                                                                                                                                                              |
| duration_in_months (integer) | If `duration` is `repeating`, the number of months the coupon applies. Null if coupon `duration` is `forever` or once.                                                                                                                                                               |
| max_redemptions (integer)    | Maximum number of times this coupon can be redeemed, in total, across all customers, before it is no longer valid.                                                                                                                                                                   |
| percent_off (integer)        | Percent that will be taken off the subtotal of any invoices for this customer for the duration of the coupon. For example, a coupon with percent_off of 50 will make a $100 invoice $50 instead.                                                                                     |
| redeem_by (datetime)         | Date after which the coupon can no longer be redeemed.                                                                                                                                                                                                                               |
| times_redeemed (integer)     | Number of times this coupon has been applied to a customer.                                                                                                                                                                                                                          |
| valid (boolean)              | Taking account of the above properties, whether this coupon can still be applied to a customer.                                                                                                                                                                                      |
| date_purged (datetime)       | Deleted at datetime by which we can determine when the coupon was deleted. When a coupon is deleted on stripe this field will be updated.                                                                                                                                            |
| metadata (json)              | Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. |
| livemode (boolean)           | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                                                                                                                                                                           |

### Configuration

Once the `Coupon` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "COUPON_MODEL": "app.models.Coupon"
}
```

## Event

Events are updates from Stripe to a backend system that are triggered whenever changes occur on the Stripe side. To define an event model that includes all the fields found in a Stripe event object, developers can inherit from `StripeBaseEvent` provided by the library.

!!! Example
    ```python
    from stripe_integrations.models import StripeBaseEvent


    class Event(StripeBaseEvent):
        pass
    ```

### Fields

The `StripeBaseEvent` abstract model provides the following fields:

| Field                      | Description                                                                                                                       |
| -------------------------- |-----------------------------------------------------------------------------------------------------------------------------------|
| id (string)                | The primary key id (uuid) of the event in the local database.                                                                     |
| created_at (datetime)      | Timestamp when the event object was created in the local database.                                                                |
| updated_at (datetime)      | Timestamp when the event object was last updated in the local database.                                                           |
| stripe_id (string)         | Stripe object id                                                                                                                  |
| kind (string)              | the label of the event                                                                                                            |
| webhook_message (json)     | request data that the webhook recieve from stripe.                                                                                |
| validated_message (json)   | The validated event message is stored in this field                                                                               |
| valid (boolean)            | Store whether the event was valid or not.                                                                                         |
| processed (boolean)        | Status of event, whether the event was proccessed or not.                                                                         |
| request (json)             | Information on the API request that instigated the event.                                                                         |
| pending_webhooks (integer) | Number of webhooks that have yet to be successfully delivered (i.e., to return a 20x response) to the URLs you’ve specified.      |
| api_version (string)       | The Stripe API version used to render `data`. <br> Note: This property is populated only for events on or after October 31, 2014. |
| livemode (boolean)         | Has the value true if the object exists in live mode or the value false if the object exists in test mode.                        |

### Configuration

Once the `Event` model is created. Add the model path in `STRIPE_CONFIG`.

```python
STRIPE_CONFIG = {
    ...
    "EVENT_MODEL": "app.models.Event"
}
```

## Database migration

After implementing the models, create a migration file using the following command:

```commandline
python manage.py makemigrations
```

Once the migration file has been created, apply the migrations to the database using the following command:

```commandline
python manage.py migrate
```
