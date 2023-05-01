# Stripe Integrations

__Version:__ 0.0.1

`stripe-integrations` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Management commands that help synchronize customer data, cards, subscriptions, coupons, prices, and products from Stripe.
- Built-in webhook handling for secure communication with Stripe.
- A wide range of functions for creating and managing customers, subscriptions, and other Stripe-related operations within your Django web application.

## Installation

You can easily install or upgrade to the latest version of the package using pip:

```
pip install stripe-integrations
```

## Configuration

In your settings, update `STRIPE_CONFIG`:

```python
STRIPE_CONFIG = {
    "API_VERSION": "2022-11-15", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
    "CUSTOMER_MODEL": "project_name.app.models.Customer", # Path to import Stripe Customer model
    "CARD_MODEL": "project_name.app.models.Card", # Path to import Stripe Card model
    "PRODUCT_MODEL": "project_name.app.models.Product", # Path to import Stripe Product model
    "PRICE_MODEL": "project_name.app.models.Price", # Path to import Stripe Price model
    "COUPON_MODEL": "project_name.app.models.Coupon", # Path to import Stripe Coupon model
    "EVENT_MODEL": "project_name.app.models.Event", # Path to import Stripe Event model
    "SUBSCRIPTION_MODEL": "project_name.app.models.Subscription", # Path to import Stripe Subscription model
    "CUSTOMER_FIELD_NAME": "customer", # Field name used to have foreign key relation with `Customer` model
    "USER_FIELD_NAME": "user", # Field name that is used by `Customer` model to have foreign relation to `User` model
}
```

## References

Stripe API Doc: [https://stripe.com/docs/api](https://stripe.com/docs/api)
