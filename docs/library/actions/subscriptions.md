# Subscription

Actions related to subscriptions in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeSubscription

    StripeSubscription.sync_from_stripe_data(customer, stripe_subscription)
    ```

## Create subscription

Creates a subscription for the given customer.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.create(customer, prices)
```

***Returns***

Local Subscription object

**Arguments**

| Argument                   | Description                                                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| customer                   | Customer object                                                                                    |
| prices                     | List of stripe price id                                                                            |
| coupon (Optional)          | Coupon object.  <br>Default:`None`                                                                 |
| trial_from_plan (Optional) | Indicates if a plan’s trial_period_days should be applied to the subscription. <br>Default: `True` |


## Update subscription

Updates a subscription.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.update(subscription, price)
```

***Returns***

Local Subscription object

**Arguments**

| Argument                | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| subscription            | Subscription object                                          |
| price                   | Price object to be subscribed to                             |
| subscription (Optional) | Whether to prorate Subscription charges. <br>Default: `True` |


## Cancel subscription

Cancels the subscription. It will cancel the subscription at the end of the current billing period. To cancel the subscription immediately pass `cancel_immediately` as `True` in the argument.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.cancel(subscription)
```

***Returns***

Local Subscription object

**Arguments**

| Argument                      | Description                                                           |
| ----------------------------- | --------------------------------------------------------------------- |
| subscription                  | Subscription object                                                   |
| cancel_immediately (Optional) | Whether to cancel the subscription immediately. <br> Default: `False` |

## Sync customer from stripe data

Synchronizes data from the Stripe API for a subscription.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.sync_from_stripe_data(customer, stripe_subscription)
```

***Returns***

Local Subscription object

**Arguments**

| Argument            | Description                                              |
| ------------------- | -------------------------------------------------------- |
| customer            | Customer's object                                        |
| stripe_subscription | Stripe subscription object that returned from stripe API |

## Check if customer has active subscription

Checks if the given customer has an active subscription

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.has_active_subscription(customer)
```

***Returns***

Boolean(True or False)

**Arguments**

| Argument | Description       |
| -------- | ----------------- |
| customer | Customer's object |

## Get current subscription

Get current subscription for a given user

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.get_current_subscription(user)
```

***Returns***

Local Subscription object

**Arguments**

| Argument            | Description                           |
| ------------------- | ------------------------------------- |
| user                | User's object                         |
| customer (Optional) | Customer's object <br>Default: `None` |

!!! Note
    If customer is not passed it will fetch the customer detail.

## Retrieve subscription

Retrieve latest subscription detail for a given user.

!!! Info
    First it will check for current subscription it current subscription is not available then it will return the latest subscription.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.get_current_subscription(user)
```

***Returns***

Local Subscription object

**Arguments**

| Argument            | Description                           |
| ------------------- | ------------------------------------- |
| user                | User's object                         |
| customer (Optional) | Customer's object <br>Default: `None` |

!!! Note
    If cutomer is not passed it will fetch the customer detail.

## Retrieve stripe subscription object

Retrieve stripe subscription object for a given subscription.

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.get_stripe_subscription(subscription)
```

***Returns***

Stripe subscription object

**Arguments**

| Argument     | Description         |
| ------------ | ------------------- |
| subscription | Subscription object |

## Get upcoming invoice

Get upcoming stripe invoice object for a given subscription

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.get_upcoming_invoice(subscription)
```

***Returns***

Stripe invoice object

**Arguments**

| Argument     | Description         |
| ------------ | ------------------- |
| subscription | Subscription object |

## Get latest invoice

Get latest stripe invoice object for a given subscription

**Method**

```python
from stripe_integrations.actions import StripeSubscription

StripeSubscription.get_latest_invoice(subscription)
```

***Returns***

Stripe invoice object

**Arguments**

| Argument     | Description         |
| ------------ | ------------------- |
| subscription | Subscription object |
