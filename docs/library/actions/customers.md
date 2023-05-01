# Customer

Actions related to customers in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeCustomer

    # Sync customer from Stripe
    StripeCustomer.sync(customer)
    ```

## Create customer

This functionality allows the creation of a customer on the Stripe platform. In case a customer with the same credentials already exists, the existing customer information will be returned instead.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.create(user, billing_email)
```

***Returns***

Local Customer object

**Arguments**

| Argument      | Description                   |
| ------------- | ----------------------------- |
| user          | User object                   |
| billing_email | The customer’s email address. |

!!! Note
    You can pass all the fields in the Customer model as arguments to the method, except for  `date_purged`, `is_active`, and `livemode`.
    The `billing_email` field maps to the `email` field for the Stripe customer.

## Retrieve Customer

This method retrieves the details of a customer object for a specified user.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.get(user)
```

***Returns***

Local Customer object

**Arguments**

| Argument | Description |
| -------- | ----------- |
| user     | User object |

## Sync Customer from Stripe data

This method synchronizes the local Customer object with the details obtained from the Stripe API.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.sync_from_stripe_data(customer, stripe_customer)
```

***Returns***

Local Customer object

**Arguments**

| Argument        | Description                                          |
| --------------- | ---------------------------------------------------- |
| customer        | Customer's object                                    |
| stripe_customer | Stripe customer object that returned from stripe API |

## Sync customer

This method synchronizes a local Customer object with details from Stripe. It also synchronizes the customer's default payment source (card) and subscription details.

!!! Note
    Please note that this method has a dependency on the Card and Subscription models. If these models are not implemented, the method will throw an error.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.sync(customer)
```

***Returns***

Local Customer object

**Arguments**

| Argument                   | Description                                          |
| -------------------------- | ---------------------------------------------------- |
| customer                   | Customer's object                                    |
| stripe_customer (Optional) | Stripe customer object that returned from stripe API |

!!! Note
    It will fetch the details from stripe if `stripe_customer` is not passed.

## Link customer to event

This method links the customer referred to in a webhook event message to the corresponding local Event object.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.link_customer(event)
```

***Returns***

Local Event object

**Arguments**

| Argument | Description  |
| -------- | ------------ |
| event    | Event object |

## Soft delete customer

Updates the `date_purged` and `is_active` fields of a customer object to mark it as deleted.

**Method**

```python
from stripe_integrations.actions import StripeCustomer

StripeCustomer.soft_delete(customer)
```

***Returns***

`None`

**Arguments**

| Argument | Description     |
| -------- | --------------- |
| customer | Customer object |
