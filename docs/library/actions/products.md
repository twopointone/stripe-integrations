# Product

Actions related to products in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeProduct

    StripeProduct.sync_all()
    ```

## Sync all products

Synchronizes all products from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripeProduct

StripeProduct.sync_all()
```

***Returns***

`None`

## Sync product

Synchronizes product from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripeProduct

StripeProduct.sync(product)
```

***Returns***

Local Product object, Boolean value (Whether the product object is created)

!!! Info
    It will create or update product based on stripe id.

**Arguments**

| Argument | Description                                 |
| -------- |---------------------------------------------|
| product  | Data from Stripe API representing a product |


## Soft delete product

Updates `date_purged` field to mark it as deleted.

**Method**

```python
from stripe_integrations.actions import StripeProduct

StripeProduct.soft_delete(stripe_id)
```

***Returns***

`None`

**Arguments**

| Argument  | Description         |
| --------- |---------------------|
| stripe_id | Product's Stripe ID |
