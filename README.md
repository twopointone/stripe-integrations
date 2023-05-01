# Stripe Integrations

`stripe-integrations` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Management commands that help synchronize customer data, cards, subscriptions, coupons, prices, and products from Stripe.
- Built-in webhook handling for secure communication with Stripe.
- A wide range of functions for creating and managing customers, subscriptions, and other Stripe-related operations within your Django web application.

## Table of Contents

- [💾 Installation](#-installation)
- [🚀 Quickstart](#-quickstart)
- [📜 Code of Conduct](#code-of-conduct)

## 💾 Installation

You can easily install or upgrade to the latest version of the package using pip:

```
pip install stripe-integrations
```

## 🚀 Quickstart

To get started quickly, follow these steps:

1. Install the package using pip:

```commandline
pip install stripe-integrations
```

2. Add `stripe_integrations` to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...,
    'stripe_integrations',
]
```

3. Create models to manage Stripe data using the abstract base classes provided in `stripe_integrations.models`. For example:

```python
from stripe_integrations.models import StripeBaseCustomer, StripeBaseCard, StripeBaseSubscription, StripeBaseProduct, StripeBasePrice, StripeBaseCoupon, StripeBaseEvent
from users.models import User


class Customer(StripeBaseCustomer):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stripe_customers",
    )
    # Add custom fields as per project requirement


class Card(StripeBaseCard):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    # Add custom fields as per project requirement


class Subscription(StripeBaseSubscription):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text="The customer associated with this subscription",
    )
    # Add custom fields as per project requirement


class Product(StripeBaseProduct):
    # Add custom fields as per project requirement
    pass


class Price(StripeBaseProduct):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="prices",
    )
    # Add custom fields as per project requirement


class Coupon(StripeBaseCoupon):
    # Add custom fields as per project requirement
    pass


class Event(StripeBaseEvent):
    # Add custom fields as per project requirement
    pass
```

4. Database migration

After implementing the models, create a migration file using the following command:

```
python manage.py makemigrations
```

Once the migration file has been created, apply the migrations to the database using the following command:

```
python manage.py migrate
```

5. In your settings, update the model paths in `STRIPE_CONFIG`:

```python
STRIPE_CONFIG = {
    "API_VERSION": "2022-11-15", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
    "CUSTOMER_MODEL": "project_name.app.models.Customer",
    "CARD_MODEL": "project_name.app.models.Card",
    "PRODUCT_MODEL": "project_name.app.models.Product",
    "PRICE_MODEL": "project_name.app.models.Price",
    "COUPON_MODEL": "project_name.app.models.Coupon",
    "EVENT_MODEL": "project_name.app.models.Event",
    "SUBSCRIPTION_MODEL": "project_name.app.models.Subscription",
    "CUSTOMER_FIELD_NAME": "customer", # Field name used to have foreign key relation with `Customer` model
    "USER_FIELD_NAME": "user", # Field name that is used by `Customer` model to have foreign relation to `User` model
}
```

6. Implement APIs

You can use the appropriate actions to build payment APIs. Here are some examples:

- Creating a customer

```python
from stripe_integrations.actions.customers import StripeCustomer

# Pass user model instance and email as argument
customer = StripeCustomer.create(user, billing_email)
```

- Creating a subscription

```python
from stripe_integrations.actions.subscriptions import StripeSubscription

# Pass customer model instance and prices(List of stripe price ids) to subscribe as argument
subscription = StripeSubscription.create(customer, prices)
```

## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, we have a code of conduct, which can be found [here](CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python and `stripe-integrations` with you.
