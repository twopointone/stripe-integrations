# Coupon

Actions related to coupons in Stripe that can be used for various purposes.

!!! Example
    ```python
    from stripe_integrations.actions import StripeCoupon

    StripeCoupon.sync_all()
    ```

## Sync all coupons

Synchronizes all coupons from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripeCoupon

StripeCoupon.sync_all()
```

***Returns***

`None`

## Sync coupon

Synchronizes coupon from the Stripe API

**Method**

```python
from stripe_integrations.actions import StripeCoupon

StripeCoupon.sync(stripe_coupon)
```

***Returns***

Local coupon object, Boolean value (Whether the coupon object is created)

!!! Info
    It will create or update coupon based on Stripe ID.

**Arguments**

| Argument      | Description                                |
| ------------- |--------------------------------------------|
| stripe_coupon | Data from Stripe API representing a coupon |


## Retrieve coupon

Retrieve coupon in local database.

**Method**

```python
from stripe_integrations.actions import StripeCoupon

StripeCoupon.get(stripe_id)
```

***Returns***

Local Coupon Object

**Arguments**

| Argument  | Description        |
| --------- |--------------------|
| stripe_id | Coupon's Stripe ID |


## Soft delete coupon

It will update the `date_purged` to mark it as deleted.

**Method**

```python
from stripe_integrations.actions import StripeCoupon

StripeCoupon.soft_delete(stripe_id)
```
***Returns***

`None`

**Arguments**

| Argument  | Description        |
| --------- |--------------------|
| stripe_id | Coupon's Stripe ID |
