# Price

Actions related to prices in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripePrice

    StripePrice.sync_all()
    ```

## Sync all prices

Synchronizes all prices from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripePrice

StripePrice.sync_all()
```

***Returns***

`None`

## Sync price

Synchronizes price from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripePrice

StripePrice.sync(price)
```

***Returns***

Local Price object, Boolean value (Whether the price object is created)

!!! Info
    It will create or update price based on stripe id. Also it will map the price to respective product.

**Arguments**

| Argument | Description                               |
| -------- |-------------------------------------------|
| price    | Data from Stripe API representing a price |


## Soft delete price

Update the `date_purged` field to mark it as deleted.

**Method**

```python
from stripe_integrations.actions import StripePrice

StripePrice.soft_delete(stripe_id)
```

***Returns***

`None`

**Arguments**

| Argument  | Description       |
| --------- |-------------------|
| stripe_id | Price's Stripe ID |
