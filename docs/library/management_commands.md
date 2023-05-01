# Management commands

Built-in management commands that can be used for various use cases. The following are the available commands:

## Sync customer details

Use this command to synchronize [customers](/library/models/#customer)-related details ([default source/card](/library/models/#card) and [subscriptions](/library/models/#subscription)) from Stripe to the local database. Note that it only updates existing customers; it doesn't create new ones.

```
python manage.py sync_stripe_customers
```

## Sync products

Use this command to sync products from Stripe to the local database. It updates existing [products](/library/models/#product) and creates new ones.

```
python manage.py sync_stripe_products
```

## Sync prices

Use this command to sync prices from Stripe to the local database. It updates existing [prices](/library/models/#price) and creates new ones.

```
python manage.py sync_stripe_prices
```

## Sync coupons

Use this command to sync coupons from Stripe to the local database. It updates existing [coupons](/library/models/#coupon) and creates new ones.

```
python manage.py sync_stripe_coupons
```
